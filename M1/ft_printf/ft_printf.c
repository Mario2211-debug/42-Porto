/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/03 01:56:59 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/05 19:23:46 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_printf(const char *str, ...)
{
	int		print_length;
	int		i;
	va_list	args;

	i = 0;
	print_length = 0;
	va_start(args, str);
	while (str[i])
	{
		if (str[i] == '%')
		{
			i++;
			print_length += ft_handle_print(str[i], args);
		}
		else
		{
			print_length += ft_putchar(str[i]);
		}
		i++;
	}
	va_end(args);
	return (print_length);
}
