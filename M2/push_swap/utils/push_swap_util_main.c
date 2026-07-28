/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_util_main.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 12:10:45 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/12 01:04:16 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/push_swap.h"

void	sort_algo(int *arr, int sz)
{
	int	i;
	int	j;
	int	min;
	int	min_pos;

	i = 0;
	while (i < sz - 1)
	{
		min = arr[i];
		min_pos = i;
		j = i + 1;
		while (j < sz)
		{
			if (arr[j] < min)
			{
				min = arr[j];
				min_pos = j;
			}
			j++;
		}
		if (min_pos != i)
			ft_swap(&arr[i], &arr[min_pos]);
		i++;
	}
}

int	is_error(char **argv, int argc)
{
	int	i;
	int	value;

	i = 1;
	while (i < argc)
	{
		if (!ft_atoi(argv[i], &value))
			return (1);
		i++;
	}
	return (0);
}

int	*ft_parsing(char **argv, int argc)
{
	int	*i_arr;
	int	i;
	int	value;

	i_arr = malloc(sizeof(int) * (argc - 1));
	if (!i_arr)
		return (NULL);
	i = 1;
	while (i < argc)
	{
		if (!ft_atoi(argv[i], &value))
		{
			free(i_arr);
			return (NULL);
		}
		i_arr[i - 1] = value;
		i++;
	}
	if (has_duplicate(i_arr, argc - 1))
	{
		free(i_arr);
		return (NULL);
	}
	return (i_arr);
}

int	stack_size(t_list *s)
{
	int	n;

	n = 0;
	while (s)
	{
		n++;
		s = s->next;
	}
	return (n);
}

int	has_duplicate(int *arr, int size)
{
	int	i;
	int	j;

	i = 0;
	while (i < size)
	{
		j = i + 1;
		while (j < size)
		{
			if (arr[i] == arr[j])
				return (1);
			j++;
		}
		i++;
	}
	return (0);
}
