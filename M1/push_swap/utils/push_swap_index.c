/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_index.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 11:48:23 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/12 00:01:05 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/push_swap.h"

int	get_max_bits(int sz)
{
	int	max;
	int	bits;

	max = sz - 1;
	bits = 0;
	while ((max >> bits) != 0)
		bits++;
	return (bits);
}

void	ft_swap(int *big, int *sma)
{
	int	tmp;

	tmp = 0;
	tmp = *sma;
	*sma = *big;
	*big = tmp;
}

int	ft_check(int arr[], int sz)
{
	int	i;

	i = 0;
	while (i < sz)
	{
		if (arr[i] > arr[i + 1])
			return (1);
		i++;
	}
	return (0);
}

void	index_in_stack(int *arr, int len, t_list *a)
{
	int		i;
	t_list	*curr;

	curr = a;
	i = 0;
	while (curr)
	{
		i = 0;
		while (i < len)
		{
			if (arr[i] == curr->data)
				curr->index = i;
			i++;
		}
		curr = curr->next;
	}
}

int	is_sorted(t_list *a)
{
	while (a && a->next)
	{
		if (a->index > a->next->index)
			return (0);
		a = a->next;
	}
	return (1);
}
