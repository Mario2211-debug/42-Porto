/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:32 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 19:53:46 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Initializes a dingle with its mutex, condition variable and wait queue.
*/
void	init_dongle(t_dongle *dongle, int id, t_data *data)
{
	dongle->id = id;
	dongle->is_taken = 0;
	dongle->avaliable_at = 0;
	dongle->data = data;
	pthread_cond_init(&dongle->cond, NULL);
	pthread_mutex_init(&dongle->dongle_lock, NULL);
	pq_init(&dongle->wait_queue, data->n_coders + 1);
}

/*
Destroys a dongle's mutex, condition variable and wait queue
*/
void	destroy_dongle(t_dongle *dongle)
{
	pthread_mutex_destroy(&dongle->dongle_lock);
	pthread_cond_destroy(&dongle->cond);
	pq_destroy(&dongle->wait_queue);
}

static long	get_coder_priority(t_coder *coder)
{
	if (coder->data->scheduler == SCHED_FIFO_MODE)
		return (get_time_ms());
	else
		return (coder->deadline);
}

/*
** Accquires a dongle using timedwait for predict wake-up.
** The code joins a priority queue and waits until:
** 1. The dongle is free and past cooldown.
** 2. This coder is ar the front of the queue.
** Uses timedwait with 5ms timeout gto handle cooldown expiry.
*/

void	take_dongle(t_coder *coder, t_dongle *dongle)
{
	long			priority;
	struct timespec	ts;

	pthread_mutex_lock(&dongle->dongle_lock);
	priority = get_coder_priority(coder);
	pq_push(&dongle->wait_queue, coder->id, priority);
	while (1)
	{
		if (is_sim_over(coder->data))
		{
			pthread_mutex_unlock(&dongle->dongle_lock);
			return ;
		}
		if (!dongle->is_taken && get_time_ms() >= dongle->avaliable_at
			&& pq_peek(&dongle->wait_queue) == coder->id)
		{
			pq_pop(&dongle->wait_queue);
			dongle->is_taken = 1;
			pthread_mutex_unlock(&dongle->dongle_lock);
			log_action(coder->data, coder->id, "has taken a dongle");
			return ;
		}
		ts = get_timeout(5);
		pthread_cond_timedwait(&dongle->cond, &dongle->dongle_lock, &ts);
	}
}

/*
** Releases a dongle and sets the coldown timer.
** Wakes all threads waiting on this dongle.
*/

void	release_dongle(t_coder *coder, t_dongle *dongle)
{
	pthread_mutex_lock(&dongle->dongle_lock);
	dongle->is_taken = 0;
	dongle->avaliable_at = get_time_ms() + coder->data->dongle_cooldown;
	pthread_cond_broadcast(&dongle->cond);
	pthread_mutex_unlock(&dongle->dongle_lock);
}
