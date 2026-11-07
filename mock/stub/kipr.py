import time, sys
class _P:
    def __init__(s): s.x=80; s.y=60
def msleep(ms):
    time.sleep(ms/1000/20)
def get_motor_position_counter(*a):
    print("[kipr] get_motor_position_counter"+str(a), flush=True); return 0
def gmpc(*a):
    print("[kipr] gmpc"+str(a), flush=True); return 0
def clear_motor_position_counter(*a):
    print("[kipr] clear_motor_position_counter"+str(a), flush=True); return 0
def cmpc(*a):
    print("[kipr] cmpc"+str(a), flush=True); return 0
def move_at_velocity(*a):
    print("[kipr] move_at_velocity"+str(a), flush=True); return 0
def mav(*a):
    print("[kipr] mav"+str(a), flush=True); return 0
def move_to_position(*a):
    print("[kipr] move_to_position"+str(a), flush=True); return 0
def mtp(*a):
    print("[kipr] mtp"+str(a), flush=True); return 0
def move_relative_position(*a):
    print("[kipr] move_relative_position"+str(a), flush=True); return 0
def mrp(*a):
    print("[kipr] mrp"+str(a), flush=True); return 0
def freeze(*a):
    print("[kipr] freeze"+str(a), flush=True); return 0
def get_motor_done(*a):
    print("[kipr] get_motor_done"+str(a), flush=True); return 0
def block_motor_done(*a):
    print("[kipr] block_motor_done"+str(a), flush=True); return 0
def bmd(*a):
    print("[kipr] bmd"+str(a), flush=True); return 0
def setpwm(*a):
    print("[kipr] setpwm"+str(a), flush=True); return 0
def getpwm(*a):
    print("[kipr] getpwm"+str(a), flush=True); return 0
def fd(*a):
    print("[kipr] fd"+str(a), flush=True); return 0
def bk(*a):
    print("[kipr] bk"+str(a), flush=True); return 0
def motor(*a):
    print("[kipr] motor"+str(a), flush=True); return 0
def motor_power(*a):
    print("[kipr] motor_power"+str(a), flush=True); return 0
def off(*a):
    print("[kipr] off"+str(a), flush=True); return 0
def alloff(*a):
    print("[kipr] alloff"+str(a), flush=True); return 0
def ao(*a):
    print("[kipr] ao"+str(a), flush=True); return 0
def enable_servo(*a):
    print("[kipr] enable_servo"+str(a), flush=True); return 0
def disable_servo(*a):
    print("[kipr] disable_servo"+str(a), flush=True); return 0
def enable_servos(*a):
    print("[kipr] enable_servos"+str(a), flush=True); return 0
def disable_servos(*a):
    print("[kipr] disable_servos"+str(a), flush=True); return 0
def set_servo_enabled(*a):
    print("[kipr] set_servo_enabled"+str(a), flush=True); return 0
def get_servo_enabled(*a):
    print("[kipr] get_servo_enabled"+str(a), flush=True); return 0
def get_servo_position(*a):
    print("[kipr] get_servo_position"+str(a), flush=True); return 0
def set_servo_position(*a):
    print("[kipr] set_servo_position"+str(a), flush=True); return 0
def analog(*a):
    print("[kipr] analog"+str(a), flush=True); return 0
def analog8(*a):
    print("[kipr] analog8"+str(a), flush=True); return 0
def analog10(*a):
    print("[kipr] analog10"+str(a), flush=True); return 0
def analog12(*a):
    print("[kipr] analog12"+str(a), flush=True); return 0
def digital(*a):
    print("[kipr] digital"+str(a), flush=True); return 0
def set_digital_value(*a):
    print("[kipr] set_digital_value"+str(a), flush=True); return 0
def get_digital_value(*a):
    print("[kipr] get_digital_value"+str(a), flush=True); return 0
def a_button(*a):
    print("[kipr] a_button"+str(a), flush=True); return 0
def a_button_clicked(*a):
    print("[kipr] a_button_clicked"+str(a), flush=True); return 0
def any_button(*a):
    print("[kipr] any_button"+str(a), flush=True); return 0
def b_button(*a):
    print("[kipr] b_button"+str(a), flush=True); return 0
def b_button_clicked(*a):
    print("[kipr] b_button_clicked"+str(a), flush=True); return 0
def c_button(*a):
    print("[kipr] c_button"+str(a), flush=True); return 0
def c_button_clicked(*a):
    print("[kipr] c_button_clicked"+str(a), flush=True); return 0
def extra_buttons_hide(*a):
    print("[kipr] extra_buttons_hide"+str(a), flush=True); return 0
def extra_buttons_show(*a):
    print("[kipr] extra_buttons_show"+str(a), flush=True); return 0
def x_button(*a):
    print("[kipr] x_button"+str(a), flush=True); return 0
def x_button_clicked(*a):
    print("[kipr] x_button_clicked"+str(a), flush=True); return 0
def y_button(*a):
    print("[kipr] y_button"+str(a), flush=True); return 0
def y_button_clicked(*a):
    print("[kipr] y_button_clicked"+str(a), flush=True); return 0
def z_button(*a):
    print("[kipr] z_button"+str(a), flush=True); return 0
def z_button_clicked(*a):
    print("[kipr] z_button_clicked"+str(a), flush=True); return 0
def left_button(*a):
    print("[kipr] left_button"+str(a), flush=True); return 0
def right_button(*a):
    print("[kipr] right_button"+str(a), flush=True); return 0
def camera_open(*a):
    print("[kipr] camera_open"+str(a), flush=True); return 0
def camera_open_black(*a):
    print("[kipr] camera_open_black"+str(a), flush=True); return 0
def camera_load_config(*a):
    print("[kipr] camera_load_config"+str(a), flush=True); return 0
def camera_update(*a):
    print("[kipr] camera_update"+str(a), flush=True); return 0
def get_object_count(*a):
    print("[kipr] get_object_count"+str(a), flush=True); return 0
def get_object_area(*a):
    print("[kipr] get_object_area"+str(a), flush=True); return 0
def get_object_center(*a): return _P()
def get_object_centroid(*a):
    print("[kipr] get_object_centroid"+str(a), flush=True); return 0
def get_object_confidence(*a):
    print("[kipr] get_object_confidence"+str(a), flush=True); return 0
def camera_close(*a):
    print("[kipr] camera_close"+str(a), flush=True); return 0
def create_connect(*a):
    print("[kipr] create_connect"+str(a), flush=True); return 0
def create_disconnect(*a):
    print("[kipr] create_disconnect"+str(a), flush=True); return 0
def create_drive_direct(*a):
    print("[kipr] create_drive_direct"+str(a), flush=True); return 0
def create_drive_straight(*a):
    print("[kipr] create_drive_straight"+str(a), flush=True); return 0
def create_spin_CW(*a):
    print("[kipr] create_spin_CW"+str(a), flush=True); return 0
def create_spin_CCW(*a):
    print("[kipr] create_spin_CCW"+str(a), flush=True); return 0
def create_stop(*a):
    print("[kipr] create_stop"+str(a), flush=True); return 0
def get_create_lbump(*a):
    print("[kipr] get_create_lbump"+str(a), flush=True); return 0
def get_create_rbump(*a):
    print("[kipr] get_create_rbump"+str(a), flush=True); return 0
def get_create_distance(*a):
    print("[kipr] get_create_distance"+str(a), flush=True); return 0
def get_create_total_angle(*a):
    print("[kipr] get_create_total_angle"+str(a), flush=True); return 0
def get_create_lcliff_amt(*a):
    print("[kipr] get_create_lcliff_amt"+str(a), flush=True); return 0
def get_create_rcliff_amt(*a):
    print("[kipr] get_create_rcliff_amt"+str(a), flush=True); return 0
def get_create_lfcliff_amt(*a):
    print("[kipr] get_create_lfcliff_amt"+str(a), flush=True); return 0
def get_create_rfcliff_amt(*a):
    print("[kipr] get_create_rfcliff_amt"+str(a), flush=True); return 0
def set_create_distance(*a):
    print("[kipr] set_create_distance"+str(a), flush=True); return 0
def set_create_total_angle(*a):
    print("[kipr] set_create_total_angle"+str(a), flush=True); return 0
def create3_connect(*a):
    print("[kipr] create3_connect"+str(a), flush=True); return 0
def create3_drive_straight(*a):
    print("[kipr] create3_drive_straight"+str(a), flush=True); return 0
def create3_rotate_degrees(*a):
    print("[kipr] create3_rotate_degrees"+str(a), flush=True); return 0
def create3_drive_arc_degrees(*a):
    print("[kipr] create3_drive_arc_degrees"+str(a), flush=True); return 0
def create3_velocity_set_components(*a):
    print("[kipr] create3_velocity_set_components"+str(a), flush=True); return 0
def create3_wait(*a):
    print("[kipr] create3_wait"+str(a), flush=True); return 0
def create3_dock(*a):
    print("[kipr] create3_dock"+str(a), flush=True); return 0
def create3_undock(*a):
    print("[kipr] create3_undock"+str(a), flush=True); return 0
def create3_sensor_bump(*a):
    print("[kipr] create3_sensor_bump"+str(a), flush=True); return 0
def create3_sensor_cliff(*a):
    print("[kipr] create3_sensor_cliff"+str(a), flush=True); return 0
def create3_sensor_ir(*a):
    print("[kipr] create3_sensor_ir"+str(a), flush=True); return 0
def accel_x(*a):
    print("[kipr] accel_x"+str(a), flush=True); return 0
def accel_y(*a):
    print("[kipr] accel_y"+str(a), flush=True); return 0
def accel_z(*a):
    print("[kipr] accel_z"+str(a), flush=True); return 0
def gyro_x(*a):
    print("[kipr] gyro_x"+str(a), flush=True); return 0
def gyro_y(*a):
    print("[kipr] gyro_y"+str(a), flush=True); return 0
def gyro_z(*a):
    print("[kipr] gyro_z"+str(a), flush=True); return 0
def gyro_calibrate(*a):
    print("[kipr] gyro_calibrate"+str(a), flush=True); return 0
def magneto_x(*a):
    print("[kipr] magneto_x"+str(a), flush=True); return 0
def magneto_y(*a):
    print("[kipr] magneto_y"+str(a), flush=True); return 0
def magneto_z(*a):
    print("[kipr] magneto_z"+str(a), flush=True); return 0
def power_level(*a):
    print("[kipr] power_level"+str(a), flush=True); return 0
def console_clear(*a):
    print("[kipr] console_clear"+str(a), flush=True); return 0
def beep(*a):
    print("[kipr] beep"+str(a), flush=True); return 0
def systime(*a):
    print("[kipr] systime"+str(a), flush=True); return 0
def seconds(): return time.time()
def shut_down_in(*a):
    print("[kipr] shut_down_in"+str(a), flush=True); return 0
def wait_for_light(*a):
    print("[kipr] wait_for_light"+str(a), flush=True); return 0
def wait_for_milliseconds(*a):
    print("[kipr] wait_for_milliseconds"+str(a), flush=True); return 0
def wait_for_touch(*a):
    print("[kipr] wait_for_touch"+str(a), flush=True); return 0
def wait_for_a_button(*a):
    print("[kipr] wait_for_a_button"+str(a), flush=True); return 0
def wait_for_b_button(*a):
    print("[kipr] wait_for_b_button"+str(a), flush=True); return 0
def wait_for_c_button(*a):
    print("[kipr] wait_for_c_button"+str(a), flush=True); return 0
def wait_for_x_button(*a):
    print("[kipr] wait_for_x_button"+str(a), flush=True); return 0
def wait_for_y_button(*a):
    print("[kipr] wait_for_y_button"+str(a), flush=True); return 0
def wait_for_z_button(*a):
    print("[kipr] wait_for_z_button"+str(a), flush=True); return 0
def wait_for_side_button(*a):
    print("[kipr] wait_for_side_button"+str(a), flush=True); return 0
def wait_for_any_button(*a):
    print("[kipr] wait_for_any_button"+str(a), flush=True); return 0
def wait_for_a_button_clicked(*a):
    print("[kipr] wait_for_a_button_clicked"+str(a), flush=True); return 0
def wait_for_b_button_clicked(*a):
    print("[kipr] wait_for_b_button_clicked"+str(a), flush=True); return 0
def wait_for_c_button_clicked(*a):
    print("[kipr] wait_for_c_button_clicked"+str(a), flush=True); return 0
def wait_for_x_button_clicked(*a):
    print("[kipr] wait_for_x_button_clicked"+str(a), flush=True); return 0
def wait_for_y_button_clicked(*a):
    print("[kipr] wait_for_y_button_clicked"+str(a), flush=True); return 0
def wait_for_z_button_clicked(*a):
    print("[kipr] wait_for_z_button_clicked"+str(a), flush=True); return 0
