/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 17:18:14 by mafonso           #+#    #+#             */
/*   Updated: 2026/08/04 19:57:18 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libcodexion.h"

void	acquire_dongles(t_coder *coder)
{
	t_dongle	*first;
	t_dongle	*second;

	if (coder->left_dongle->id < coder->right_dongle->id)
	{
		first = coder->left_dongle;
		second = coder->right_dongle;
	}
	else
	{
		first = coder->right_dongle;
		second = coder->left_dongle;
	}
	take_dongle(coder, first);
	if (is_sim_over(coder->data))
		return ;
	take_dongle(coder, second);
}

void	release_dongles(t_coder *coder)
{
	release_dongle(coder, coder->left_dongle);
	release_dongle(coder, coder->right_dongle);
}

void	do_compile(t_coder *coder)
{
	acquire_dongles(coder);
	if (is_sim_over(coder->data))
		return ;
	pthread_mutex_lock(&coder->coder_lock);
	coder->last_compile_start = get_elapsed_ms(coder->data);
	coder->deadline = coder->last_compile_start + coder->data->tt_butnout;
	coder->status = STATE_THINKING;
	pthread_mutex_unlock(&coder->coder_lock);
	pthread_mutex_lock(&coder->coder_lock);
	coder->status = STATE_COMPILING;
	pthread_mutex_unlock(&coder->coder_lock);
	log_action(coder->data, coder->id, "is compiling");
	precise_usleep(coder->data->tt_compile, coder->data);
	release_dongles(coder);
	pthread_mutex_lock(&coder->coder_lock);
	if (!is_sim_over(coder->data))
		coder->compiles_done++;
	pthread_mutex_unlock(&coder->coder_lock);
}

void	do_debug(t_coder *coder)
{
	pthread_mutex_lock(&coder->coder_lock);
	coder->status = STATE_DEBUGGING;
	pthread_mutex_unlock(&coder->coder_lock);
	log_action(coder->data, coder->id, "is debugging");
	precise_usleep(coder->data->tt_debug, coder->data);
}

void	do_refractor(t_coder *coder)
{
	pthread_mutex_lock(&coder->coder_lock);
	coder->status = STATE_REFACTORING;
	pthread_mutex_unlock(&coder->coder_lock);
	log_action(coder->data, coder->id, "is refactoring");
	precise_usleep(coder->data->tt_refractor, coder->data);
}
