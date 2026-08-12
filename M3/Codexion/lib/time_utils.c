/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 19:03:00 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 18:32:34 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Returns a timespec for use with pthread_cond_timedwait,
** se to 'ms' milliseconds from now.
*/
struct timespec	get_timeout(long ms)
{
	struct timeval	tv;
	struct timespec	ts;

	gettimeofday(&tv, NULL);
	ts.tv_sec = tv.tv_sec + (tv.tv_usec / 1000 + ms) / 1000;
	ts.tv_nsec = ((tv.tv_usec / 1000 + ms) % 1000) * 1000000L;
	return (ts);
}

/*
** Return current time in miliseconds since epoch.
*/

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return ((long)tv.tv_sec * 1000L + (long)tv.tv_usec / 1000L);
}

/*
** Returns elapsed miliseconds since the simulation started.
*/

long	get_elapsed_ms(t_data *data)
{
	return (get_time_ms() - data->start_time);
}

/*
** Sleeps for duration_ms miliseconds, checking every "500us"
** if the simulation has ended.
*/

void	precise_usleep(long duration_ms, t_data *data)
{
	long	start;
	long	elapsed;

	start = get_time_ms();
	while (!is_sim_over(data))
	{
		elapsed = get_time_ms() - start;
		if (elapsed >= duration_ms)
			break ;
		if (duration_ms - elapsed > 2)
			usleep(500);
		else
			usleep(500);
	}
}
