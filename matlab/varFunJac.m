%% calculating the function and jacobi for self decided position data

% the variables for the angles, you differentiate for those!
syms mcp_I dip_I mcp_M dip_M mcp_R dip_R mcp_P dip_P;   

b = varAngToBm_sym([mcp_I dip_I mcp_M dip_M mcp_R dip_R mcp_P dip_P], 4, 4);

jac = jacobian(b,[mcp_I dip_I mcp_M dip_M mcp_R dip_R mcp_P dip_P]);