/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/03 20:41:01 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 18:40:07 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex(unsigned long long n, char str)
{
	int		len;
	char	*hex;

	len = 0;
	if (str == 'X')
	{
		hex = "0123456789ABCDEF";
	}
	else if (str == 'x')
	{
		hex = "0123456789abcdef";
	}
	if (n >= 16)
		len += ft_puthex(n / 16, str);
	len += ft_putchar(hex[n % 16]);
	return (len);
}
