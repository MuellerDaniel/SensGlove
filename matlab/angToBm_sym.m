%% for arbitrary sensor-finger(magnet) combinations...

function bS = angToBm_sym(theta, n_sensors, n_magnets)

% allocate memory for symbolic formula
syms x      % temporary symbolic value
b = formula(symfun(ones(n_sensors*3,1),x));     % for the resulting b-field

s_cnt = 1;      % indicates the actual sensorposition (1=sIndex, 2=sMiddle, ...)
for s = 1:3:n_sensors*3     % go through all sensors
    b_temp = formula(symfun(zeros(3,1),x));         % for the temporary/actual sensor specific b-field
    m_cnt = 1;      % indicates the actual magnet number (1=index, 2=middle, ...)    
    for m = 1:2:n_magnets*2     % sum over all the magnets        
        % m indicates the actual finger angles   
        b_temp = b_temp + angToB_sym(theta(m:m+1),s_cnt,m_cnt);
        m_cnt = m_cnt+1;
    end
    b(s:s+2) = b_temp;
    s_cnt = s_cnt+1;
end

bS = b;



%% idea behind it:
%
% bS = [angToB_sym([theta(1) theta(2)]) + ...
%       angToB_sym([theta(3) theta(4)]) + ...
%       angToB_sym([theta(5) theta(6)]) + ...
%       angToB_sym([theta(7) theta(8)]);
%       
%       angToB_sym([theta(1) theta(2)]) + ...
%       angToB_sym([theta(3) theta(4)]) + ...
%       angToB_sym([theta(5) theta(6)]) + ...
%       angToB_sym([theta(7) theta(8)]);
%       
%       angToB_sym([theta(1) theta(2)]) + ...
%       angToB_sym([theta(3) theta(4)]) + ...
%       angToB_sym([theta(5) theta(6)]) + ...
%       angToB_sym([theta(7) theta(8)]);
%       
%       angToB_sym([theta(1) theta(2)]) + ...
%       angToB_sym([theta(3) theta(4)]) + ...
%       angToB_sym([theta(5) theta(6)]) + ...
%       angToB_sym([theta(7) theta(8)])];



