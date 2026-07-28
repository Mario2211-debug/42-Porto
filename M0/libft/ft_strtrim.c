/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/03 19:57:00 by mafonso           #+#    #+#             */
/*   Updated: 2025/11/03 20:12:23 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "libft.h"

int	is_in_set(char c, const char *set)
{
	while (*set)
	{
		if (c == *set)
			return (1);
		set++;
	}
	return (0);
}

char	*ft_strtrim(char const *s1, const char *set)
{
	char	*str;
	int		i;
	int		j;
	int		len;

	i = 0;
	j = 0;
	if (!s1 || !set)
		return (NULL);
	len = ft_strlen(s1) - 1;
	while (s1[i] && is_in_set(s1[i], set))
		i++;
	while (len >= i && is_in_set(s1[len], set))
		len--;
	str = malloc(len - i + 2);
	if (!str)
		return (NULL);
	while (i <= len)
		str[j++] = s1[i++];
	str[j] = '\0';
	return (str);
}
