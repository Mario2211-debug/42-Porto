/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:14 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/08 10:59:43 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

/*
** Execute one full cycle: compile, debug, refactor
** Returns 1 if simulation should stop, 0 otherwise
*/
static int	execute_cycle(t_coder *coder)
{
	do_compile(coder);
	if (is_sim_over(coder->data))
		return (1);
	do_debug(coder);
	if (is_sim_over(coder->data))
		return (1);
	do_refractor(coder);
	if (is_sim_over(coder->data))
		return (1);
	if (coder->compiles_done >= coder->data->compiles_required)
		return (1);
	return (0);
}

void	*coder_routine(void *arg)
{
	t_coder		*coder;

	coder = (t_coder *)arg;
	pthread_mutex_lock(&coder->coder_lock);
	coder->last_compile_start = coder->data->start_time;
	coder->deadline = coder->data->start_time + coder->data->tt_butnout;
	pthread_mutex_unlock(&coder->coder_lock);
	while (!is_sim_over(coder->data))
	{
		if (execute_cycle(coder))
			break ;
	}
	return (NULL);
}
