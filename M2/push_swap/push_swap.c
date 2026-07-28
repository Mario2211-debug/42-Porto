/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/21 18:56:24 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/12 02:32:29 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "include/push_swap.h"

int	main(int argc, char **argv)
{
	int		*arr;
	t_list	*stack_a;
	t_list	*stack_b;

	arr = NULL;
	stack_a = NULL;
	stack_b = NULL;
	if (argc < 2)
		return (0);
	arr = ft_parsing(argv, argc);
	if (!arr)
		return (write(2, "Error\n", 6), 1);
	stack_a = fill_node(arr, argc - 1);
	if (!stack_a)
		return (free(arr), 1);
	sort_algo(arr, argc - 1);
	index_in_stack(arr, argc - 1, stack_a);
	free(arr);
	push_swap(&stack_a, &stack_b, argc - 1);
	free_stack(&stack_a);
	free_stack(&stack_b);
	return (0);
}
