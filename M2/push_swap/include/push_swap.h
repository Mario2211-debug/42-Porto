/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 14:09:14 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/12 01:38:49 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdio.h>
# include <stdarg.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_list
{
	int				data;
	int				index;
	struct s_list	*next;
}	t_list;
t_list	*new_node(int d);
	/* Utils */
int		ft_atoi(const char *str, int *out);
int		ft_isint(char *str);
int		is_sorted(t_list *a);
int		stack_size(t_list *s);
int		is_error(char **argv, int argc);
int		ft_check(int arr[], int sz);
int		has_duplicate(int *arr, int size);
int		get_max_bits(int sz);
int		*ft_parsing(char **argv, int as);
void	index_in_stack(int *arr, int len, t_list *stack_a);
void	push_swap(t_list **a, t_list **b, int size);
void	radix_sort(t_list **a, t_list **b, int size);
void	sort_5(t_list **a, t_list **b);
void	*fill_node(int *arr, int as);
void	ft_swap(int *big, int *sma);
void	sort_algo(int *arr, int sz);
void	free_stack(t_list **stack_a);
void	sort_3(t_list **a);
// Swap
void	sa(t_list **a);
// Push
void	pa(t_list **a, t_list **b);
void	pb(t_list **a, t_list **b);
// Rotate
void	ra(t_list **a);
void	rb(t_list **b);
void	rr(t_list **a, t_list **b);
// Rotate Rotate
void	rra(t_list **a);
void	rrb(t_list **b);
void	rrr(t_list **a, t_list **b);
#endif
