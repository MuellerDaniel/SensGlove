%% for arbitrary sensor-finger(magnet) combinations...

function bS = varAngToBm_A_sym(theta, n_sensors, n_magnets)

% allocate memory for symbolic formula
syms x      % temporary symbolic value
b = formula(symfun(ones(n_sensors*3,1),x));     % for the resulting b-field

s_cnt = 1;      % indicates the actual sensorposition (1=sIndex, 2=sMiddle, ...)
for s = 1:3:n_sensors*3     % go through all sensors
    b_temp = formula(symfun(zeros(3,1),x));         % for the temporary/actual sensor specific b-field
    m_cnt = 1;      % indicates the actual magnet number (1=index, 2=middle, ...)    
    for m = 1:3:n_magnets*3     % sum over all the magnets        
        % m indicates the actual finger angles   
        disp('theta values:');
        theta(m:m+2)
        b_temp = b_temp + varAngToB_A_sym(theta(m:m+2),s_cnt,m_cnt);
        m_cnt = m_cnt+1;
    end
    b(s:s+2) = b_temp;
    s_cnt = s_cnt+1;
end

bS = b;



