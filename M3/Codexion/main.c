/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:56 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 20:04:44 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libcodexion.h"

static int	start_threads(t_data *data)
{
	int	i;

	data->start_time = get_time_ms();
	i = 0;
	while (i < data->n_coders)
	{
		if (pthread_create(&data->coders[i].thread_id, NULL, coder_routine,
				&data->coders[i]) != 0)
		{
			fprintf(stderr, "Error: failed to create coder thread\n");
			return (1);
		}
		i++;
	}
	if (pthread_create(&data->monitor_thread, NULL, monitor_routine, data) != 0)
	{
		fprintf(stderr, "Error: failed to create monitor thread\n");
		return (1);
	}
	return (0);
}

static void	join_threads(t_data *data)
{
	int	i;

	pthread_join(data->monitor_thread, NULL);
	i = 0;
	while (i < data->n_coders)
	{
		pthread_join(data->coders[i].thread_id, NULL);
		i++;
	}
}

int	main(int argc, char **argv)
{
	t_data	data;

	memset(&data, 0, sizeof(t_data));
	if (parse_args(&data, argc, argv))
		return (1);
	if (init_simulation(&data))
		return (1);
	if (start_threads(&data))
	{
		cleanup_simulation(&data);
		return (1);
	}
	join_threads(&data);
	cleanup_simulation(&data);
	return (0);
}
