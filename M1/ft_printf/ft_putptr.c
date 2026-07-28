/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 15:22:23 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 20:48:54 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putptr(void *ptr)
{
	unsigned long long	addr;
	int					len;

	addr = (unsigned long long)ptr;
	len = 0;
	if (addr == 0)
		return (len += write(1, "(nil)", 5));
	len += write(1, "0x", 2);
	len += ft_puthex(addr, 'x');
	return (len);
}
