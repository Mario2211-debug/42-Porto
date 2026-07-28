/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_unsigned.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/03 20:39:37 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 15:14:54 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr_unsigned(unsigned int n)
{
	int	len;

	len = 0;
	if (n >= 10)
	{
		len += ft_putnbr_unsigned(n / 10);
	}
	len += ft_putchar('0' + (n % 10));
	return (len);
}
