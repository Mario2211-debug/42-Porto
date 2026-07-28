/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mafonso <mafonso@student.42porto.com>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 21:46:48 by mafonso           #+#    #+#             */
/*   Updated: 2025/12/10 18:40:37 by mafonso          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdio.h>
# include <stdarg.h>
# include <unistd.h>

int	ft_putstr(const char *str);
int	ft_printf(const char *str, ...);
int	ft_putchar(int c);
int	ft_handle_print(char str, va_list args);
int	ft_putnbr(int nb);
int	ft_putnbr_unsigned(unsigned int n);
int	ft_puthex(unsigned long long n, char str);
int	ft_putptr(void *ptr);

#endif
