/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:48 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 20:15:17 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Check if the simulation has ended thread-safe.
*/

int	is_sim_over(t_data *data)
{
	int	over;

	pthread_mutex_lock(&data->sim_mutex);
	over = data->sim_over;
	pthread_mutex_unlock(&data->sim_mutex);
	return (over);
}

/*
** Set the simulation as over (thread-safe).
*/

void	set_sim_over(t_data *data)
{
	pthread_mutex_lock(&data->sim_mutex);
	data->sim_over = 1;
	pthread_mutex_unlock(&data->sim_mutex);
}

void	cleanup_simulation(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->n_coders)
	{
		pthread_mutex_destroy(&data->coders[i].coder_lock);
		i++;
	}
	i = 0;
	while (i < data->n_coders)
	{
		destroy_dongle(&data->dongles[i]);
		i++;
	}
	pthread_mutex_destroy(&data->sim_mutex);
	pthread_mutex_destroy(&data->log_mutex);
	free(data->coders);
	free(data->dongles);
}
