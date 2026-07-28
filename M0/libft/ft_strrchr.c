/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 20:42:17 by mafonso           #+#    #+#             */
/*   Updated: 2025/11/12 16:37:26 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	int	i;
	int	cp;

	i = 0;
	cp = -1;
	while ((unsigned char)s[i] != '\0')
	{
		if ((unsigned char)s[i] == (unsigned char)c)
		{
			cp = i;
		}
		i++;
	}
	if ((unsigned char)c == '\0')
		return ((char *)(s + i));
	if (cp != -1)
		return ((char *)(s + cp));
	return (NULL);
}
