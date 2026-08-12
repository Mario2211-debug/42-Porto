/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   priority_queue.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:46 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 21:05:50 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Initialize a priority queue with the given capacity.
** Returns 0 on sucess, 1 on failure.
*/

int	pq_init(t_pqueue *pq, int capacity)
{
	pq->nodes = malloc(sizeof(t_pq_node) * capacity);
	if (!pq->nodes)
		return (1);
	pq->size = 0;
	pq->capacity = capacity;
	pthread_mutex_init(&pq->lock, NULL);
	return (0);
}

/*
** Destroys a priority queue and frees its resouces.
*/
void	pq_destroy(t_pqueue *pq)
{
	pthread_mutex_destroy(&pq->lock);
	free(pq->nodes);
	pq->nodes = NULL;
	pq->size = 0;
}

/*
** Pushes a coder onto the priority queue with given priority.
** For FIFO, priority  = arrival timestamp.
** For EDF, priority = deadline (last_compile_start + time_to_burnout).
*/
void	pq_push(t_pqueue *pq, int coder_id, long priority)
{
	if (pq->size >= pq->capacity)
		return ;
	pq->nodes[pq->size].coder_id = coder_id;
	pq->nodes[pq->size].priority = priority;
	pq->nodes[pq->size].tie_breaker = coder_id;
	pq->size++;
	pq_sift_up(pq, pq->size - 1);
}

/*
** Pop returns the highest-priority (lowest-value) coder from the queue.
** Returns the coder_id, or -1 if the queue is empty.
*/

int	pq_pop(t_pqueue *pq)
{
	int	coder_id;

	if (pq->size == 0)
		return (-1);
	coder_id = pq->nodes[0].coder_id;
	pq->size--;
	if (pq->size > 0)
	{
		pq->nodes[0] = pq->nodes[pq->size];
		pq_sift_down(pq, 0);
	}
	return (coder_id);
}

/*
** Peeks at the highest-priority coder widhout removing
** Returns the coder_id, or -1 if the queue is empty.
*/

int	pq_peek(t_pqueue *pq)
{
	if (pq->size == 0)
		return (-1);
	return (pq->nodes[0].coder_id);
}
