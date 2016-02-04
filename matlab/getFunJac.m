%% calculating the function and jacobi for given position data

syms mcp_I dip_I ...
    mcp_M dip_M ...
    mcp_R dip_R ...
    mcp_P dip_P

b = angToBm_sym([mcp_I dip_I mcp_M dip_M mcp_R dip_R mcp_P dip_P], 4, 4);

jac = jacobian(b,[mcp_I dip_I mcp_M dip_M mcp_R dip_R mcp_P dip_P]);