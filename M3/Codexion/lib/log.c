/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:39 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 19:54:25 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

void	log_action(t_data *data, int coder_id, const char *action)
{
	long	timestamp;

	pthread_mutex_lock(&data->log_mutex);
	if (!is_sim_over(data) || strcmp(action, "burned out") == 0)
	{
		timestamp = get_elapsed_ms(data);
		printf("%ld %d %s\n", timestamp, coder_id, action);
	}
	pthread_mutex_unlock(&data->log_mutex);
}
