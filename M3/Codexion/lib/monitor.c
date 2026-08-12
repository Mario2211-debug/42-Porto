/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:41 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/08 10:59:14 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Check if a single coder hasburned out.
** Returns 1 if burned out, 0 otherwise.
*/
static int	check_coder_burnout(t_coder *coder)
{
	long	now;
	long	time_since_compile;
	int		status;
	long	last_start;
	int		done;

	pthread_mutex_lock(&coder->coder_lock);
	status = coder->status;
	last_start = coder->last_compile_start;
	done = coder->compiles_done;
	pthread_mutex_unlock(&coder->coder_lock);
	if (status != STATE_THINKING)
		return (0);
	now = get_time_ms();
	if (last_start == 0)
		return (0);
	time_since_compile = now - last_start;
	if (time_since_compile >= coder->data->tt_butnout)
	{
		if (done >= coder->data->compiles_required)
			return (0);
		return (1);
	}
	return (0);
}

/*
** Check if all coders have net the required compile count.
*/
static int	all_done(t_data *data)
{
	int		i;
	int		done;

	i = 0;
	while (i < data->n_coders)
	{
		pthread_mutex_lock(&data->coders[i].coder_lock);
		done = data->coders[i].compiles_done;
		pthread_mutex_unlock(&data->coders[i].coder_lock);
		if (done < data->compiles_required)
			return (0);
		i++;
	}
	return (1);
}

/*
** Wake up all dongles condition variables so blocked coders can exit
*/
static void	wake_all_dongles(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->n_coders)
	{
		pthread_mutex_lock(&data->dongles[i].dongle_lock);
		pthread_cond_broadcast(&data->dongles[i].cond);
		pthread_mutex_unlock(&data->dongles[i].dongle_lock);
		i++;
	}
}
/*
static void	print_progress(t_data *data)
{
	int i;
	int total = 0;

	printf("\n=== PROGRESS ===\n");
	for (i = 0; i < data->n_coders; i++) {
		printf("Coder %d: %d/%d compiles\n",
		data->coders[i].id,
		data->coders[i].compiles_done,
				data->compiles_required);
				total += data->coders[i].compiles_done;
			}
			printf("Total: %d/%d compiles\n", total, data->n_coders
				* data->compiles_required);
			printf("================\n\n");
		}
*/

/*
** Check all coders for burnout. Returns 1 if someone burned out.
*/
static int	check_all_coders_burnout(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->n_coders)
	{
		if (check_coder_burnout(&data->coders[i]))
		{
			log_action(data, data->coders[i].id, "burned out");
			if (data->n_coders == 1)
				set_sim_over(data);
			set_sim_over(data);
			pthread_mutex_lock(&data->sim_mutex);
			data->someone_burned = 1;
			pthread_mutex_unlock(&data->sim_mutex);
			wake_all_dongles(data);
			return (1);
		}
		i++;
	}
	return (0);
}

/*
** The monitor thread. Runs continuosly, checking every 1ms~ whether:
** 1. A coder as burned out -> log burnout and end simulation.
** 2. All coders have completed -> end simulation.
** Burnout must be detected within 10ms of the actual event.
*/
void	*monitor_routine(void *arg)
{
	t_data	*data;

	data = (t_data *)arg;
	while (!is_sim_over(data))
	{
		if (check_all_coders_burnout(data))
			return (NULL);
		if (all_done(data))
		{
			set_sim_over(data);
			wake_all_dongles(data);
			return (NULL);
		}
		usleep(500);
	}
	return (NULL);
}
