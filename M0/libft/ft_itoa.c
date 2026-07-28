/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 19:51:55 by mafonso           #+#    #+#             */
/*   Updated: 2025/11/12 16:19:55 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	numlen(int n)
{
	long	num;
	int		length;

	length = 0;
	num = n;
	if (num <= 0)
	{
		length++;
		num = -num;
	}
	while (num != 0)
	{
		num /= 10;
		length++;
	}
	return (length);
}

char	*ft_itoa(int n)
{
	int		len;
	char	*result;
	long	num;

	num = n;
	len = numlen(n);
	result = ft_calloc(len + 1, sizeof(char));
	if (!result)
		return (NULL);
	result[len] = '\0';
	if (num < 0)
	{
		result[0] = '-';
		num = -num;
	}
	while (--len >= 0 && result[len] != '-')
	{
		result[len] = (num % 10) + '0';
		num /= 10;
	}
	return (result);
}
