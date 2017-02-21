def get_spaced_colors(n):
    max_value = 16581375 #255**3
    interval = max_value / n
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
        
    return ['#' + i for i in colors]

print(get_spaced_colors(8))
