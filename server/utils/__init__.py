def dms_to_dec(gps_lat):
    parts = [int(p[0]) / int(p[1]) for p in gps_lat]
    return parts[0] + parts[1] / 60 + parts[2] / 3600
