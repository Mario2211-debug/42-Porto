/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:36 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 16:29:06 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

static int	is_valid_number(const char *str)
{
	int	i;

	i = 0;
	if (!str || !str[0])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

static long	safe_atol(const char *str)
{
	long	result;
	int		i;

	if (!is_valid_number(str))
		return (-1);
	result = 0;
	i = 0;
	while (str[i])
	{
		result = result * 10 + (str[i] - '0');
		if (result > INT_MAX)
			return (-1);
		i++;
	}
	return (result);
}

int	parse_args(t_data *data, int argc, char **argv)
{
	if (argc != 9)
	{
		fprintf(stderr, "Usage %s, n_coders tt_burnout, tt_compile tt_debug"
			"tt_refractor, n_compiles_required, dungle_cooldown, schedule\n",
			argv[0]);
		return (1);
	}
	data->n_coders = (int)safe_atol(argv[1]);
	data->tt_butnout = safe_atol(argv[2]);
	data->tt_compile = safe_atol(argv[3]);
	data->tt_debug = safe_atol(argv[4]);
	data->tt_refractor = safe_atol(argv[5]);
	data->compiles_required = (int)safe_atol(argv[6]);
	data->dongle_cooldown = safe_atol(argv[7]);
	if (data->n_coders < 1 || data->tt_butnout < 1 || data->tt_compile < 1
		|| data->tt_debug < 1 || data->tt_refractor < 1
		|| data->compiles_required < 1 || data->dongle_cooldown < 0)
		return (fprintf(stderr, "Error: invalid arguments\n"), 1);
	if (strcmp(argv[8], "fifo") == 0)
		data->scheduler = SCHED_FIFO_MODE;
	else if (strcmp(argv[8], "edf") == 0)
		data->scheduler = SCHED_EDF_MODE;
	else
		return (fprintf(stderr, "Error: schedule must be fifo or edf\n"), 1);
	return (0);
}

static void	init_coders(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->n_coders)
	{
		data->coders[i].id = i + 1;
		data->coders[i].compiles_done = 0;
		data->coders[i].deadline = 0;
		data->coders[i].status = STATE_THINKING;
		data->coders[i].data = data;
		data->coders[i].right_dongle = &data->dongles[i];
		data->coders[i].left_dongle = &data->dongles[(i + 1) % data->n_coders];
		data->coders[i].last_compile_start = 0;
		pthread_mutex_init(&data->coders[i].coder_lock, NULL);
		i++;
	}
}

int	init_simulation(t_data *data)
{
	int	i;

	i = 0;
	data->sim_over = 0;
	data->someone_burned = 0;
	pthread_mutex_init(&data->log_mutex, NULL);
	pthread_mutex_init(&data->sim_mutex, NULL);
	data->coders = malloc(sizeof(t_coder) * data->n_coders);
	data->dongles = malloc(sizeof(t_dongle) * data->n_coders);
	if (!data->coders || !data->dongles)
	{
		fprintf(stderr, "Error: memory allocation failed\n");
		return (1);
	}
	i = 0;
	while (i < data->n_coders)
	{
		init_dongle(&data->dongles[i], i, data);
		i++;
	}
	init_coders(data);
	return (0);
}
