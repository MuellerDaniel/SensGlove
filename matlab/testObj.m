function y = testObj(one,two,res)
f = testFun(one,two);
y = norm((eye(3)-f*pinv(f))*res);