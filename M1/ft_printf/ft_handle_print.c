/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_handle_print.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 23:49:05 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 18:44:25 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_handle_print(const char str, va_list args)
{
	int	print_length;

	print_length = 0;
	if (str == 'c')
	{
		print_length += ft_putchar(va_arg(args, int));
	}
	else if (str == 's')
		print_length += ft_putstr(va_arg(args, char *));
	else if (str == 'd' || str == 'i')
		print_length += ft_putnbr(va_arg(args, int));
	else if (str == 'x' || str == 'X')
		print_length += ft_puthex(va_arg(args, unsigned int), str);
	else if (str == 'u')
		print_length += ft_putnbr_unsigned(va_arg(args, unsigned int));
	else if (str == 'p')
		print_length += ft_putptr(va_arg(args, void *));
	else if (str == '%')
		print_length += ft_putchar('%');
	return (print_length);
}
