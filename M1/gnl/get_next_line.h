/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 20:07:39 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/19 22:49:51 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H
# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif
# include <stdlib.h>
# include <unistd.h>
# include <fcntl.h>

int		ft_strlen(const char *str);
char	*get_next_line(int fd);
char	*ft_read_line(char **buffer, char **acc);
char	*str_join(char *s1, char *s2, size_t len2);
char	*ft_strdup(const char *s);
char	*ft_strchr(const char *s, int c);
char	*ft_cut_save(char **buffer, char **acc, char *newline_pos);
void	*ft_memcpy(void *dst, const void *src, size_t num);
void	*free_gnl(char **buffer, char **acc);
#endif
