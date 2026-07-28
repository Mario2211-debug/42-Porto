/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_sort_cases.c                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/11 23:02:49 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/11 23:52:33 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/push_swap.h"

void	sort_2(t_list **a)
{
	if ((*a)->index > (*a)->next->index)
		sa(a);
}

void	sort_3(t_list **a)
{
	int	a1;
	int	a2;
	int	a3;

	a1 = (*a)->index;
	a2 = (*a)->next->index;
	a3 = (*a)->next->next->index;
	if (a1 > a2 && a2 < a3 && a1 < a3)
		sa(a);
	else if (a1 > a2 && a2 < a3 && a1 > a3)
		ra(a);
	else if (a1 > a2 && a2 > a3)
	{
		sa(a);
		rra(a);
	}
	else if (a1 < a2 && a2 > a3 && a1 < a3)
	{
		sa(a);
		ra(a);
	}
	else if (a1 < a2 && a2 > a3 && a1 > a3)
		rra(a);
}

int	pos_of_min(t_list *a)
{
	int	pos;
	int	min_pos;
	int	min_idx;

	pos = 0;
	min_pos = 0;
	min_idx = a->index;
	while (a)
	{
		if (a->index < min_idx)
		{
			min_idx = a->index;
			min_pos = pos;
		}
		a = a->next;
		pos++;
	}
	return (min_pos);
}

void	sort_5(t_list **a, t_list **b)
{
	int	pos;
	int	size;

	while (stack_size(*a) > 3)
	{
		pos = pos_of_min(*a);
		size = stack_size(*a);
		if (pos <= size / 2)
			while (pos-- > 0)
				ra(a);
		else
		{
			pos = size - pos;
			while (pos-- > 0)
				rra(a);
		}
		pb(a, b);
	}
	sort_3(a);
	while (*b)
		pa(a, b);
}

void	push_swap(t_list **a, t_list **b, int sz)
{
	if (sz <= 1 || is_sorted(*a))
		return ;
	if (sz == 2)
		sort_2(a);
	else if (sz == 3)
		sort_3(a);
	else if (sz <= 5)
		sort_5(a, b);
	else
		radix_sort(a, b, sz);
}
