/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 23:42:54 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 14:18:16 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(int nb)
{
	int		len;
	char	cc;
	long	n;

	n = nb;
	len = 0;
	if (n < 0)
	{
		len += write(1, "-", 1);
		n = -n;
	}
	if (n >= 10)
	{
		len += ft_putnbr(n / 10);
	}
	cc = '0' + (n % 10);
	len += write(1, &cc, 1);
	return (len);
}
