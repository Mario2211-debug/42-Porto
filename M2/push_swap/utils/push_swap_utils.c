/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/20 14:07:18 by mafonso           #+#    #+#             */
/*   Updated: 2026/03/12 02:16:06 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/push_swap.h"

static int	parse_number(const char *str, int i, int sign, int *out)
{
	long	num;

	num = 0;
	if (!(str[i] >= '0' && str[i] <= '9'))
		return (0);
	while (str[i] >= '0' && str[i] <= '9')
	{
		num = num * 10 + (str[i] - '0');
		if ((sign == 1 && num > 2147483647)
			|| (sign == -1 && (-num) < -2147483648))
			return (0);
		i++;
	}
	if (str[i] != '\0')
		return (0);
	*out = (int)(num * sign);
	return (1);
}

static int	get_sign(const char *str, int *i)
{
	int	sign;

	sign = 1;
	if (str[*i] == '+' || str[*i] == '-')
	{
		if (str[*i] == '-')
			sign = -1;
		(*i)++;
	}
	return (sign);
}

int	ft_atoi(const char *str, int *out)
{
	int	i;
	int	sign;

	if (!str || str[0] == '\0')
		return (0);
	i = 0;
	sign = get_sign(str, &i);
	return (parse_number(str, i, sign, out));
}

void	*fill_node(int *arr, int as)
{
	t_list	*first;
	t_list	*last;
	t_list	*new;
	int		i;

	i = 0;
	first = NULL;
	last = NULL;
	while (i < as)
	{
		new = malloc(sizeof (t_list));
		new->data = arr[i];
		new->next = NULL;
		if (first == NULL)
			first = new;
		else
			last->next = new;
		last = new;
		i++;
	}
	return (first);
}
