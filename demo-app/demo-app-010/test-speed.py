f_runy = 0
while f_runy < 1:

    # calculate direction and speed

    # motor_a_p.duty( -1000 .. 2000)
    # motor_a_m.duty(-1 .. 1)

    if f_runy < 0.5:
        m_duty = -1
    else:
        m_duty = 1

    p_duty = abs(f_runy * 3000) - 1500


    print('f_runy: {} m_duty: {}, p.duty: {}'.format(f_runy, m_duty, p_duty))
    f_runy += 0.1
