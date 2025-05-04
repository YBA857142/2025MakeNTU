from motor_tt import motor_tt as move
from math import pi, atan
def motor_control(c0, c1, has_cockroach, predict, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2): 
    # c0: previous coordinates
    # c1: current coordinates
    # has_cockroach: 0 if no cockroach
    # predict: 0 if not steering, -1 if left, +1 if right
    
    if (has_cockroach == 0):
        move(predict, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2)
        return predict
    else:
        theta = 10          # restart threshold in phi units
        
        phi0 = atan(c0[0] / c0[1]) * 180 / pi
        phi1 = atan(c1[0] / c1[1]) * 180 / pi
        delta_phi = phi1 - phi0
        
        '''
        back up plan
        '''
        move(2*phi1/180)
        return 2*phi1/180
        
        if delta_phi > 0:
            if phi1 > 0:
                if abs(phi1) > theta:
                    predict_new = 1
                else:
                    predict_new = -predict**2/2 + predict/2 + 1
            else:
                if abs(phi1) > theta:
                    predict_new = 1
                else:
                    predict_new = 0
        else:
            if phi1 > 0:
                if abs(phi1) > theta:
                    predict_new = -1
                else:
                    predict_new = 0
            else:
                if abs(phi1) > theta:
                    predict_new = predict**2/2 + predict/2 - 1
                else:
                    predict_new = -1
        move(predict_new, pwm_A, pwm_B, AIN1, AIN2, BIN1, BIN2)
        return predict_new