data = importdata('pairs_room2_small.csv');
data = data.data;

figure()
hold on
axis padded
axis equal
for i = 1:length(data)
    st = data(i,1:2);
    en = data(i,3:4);
    plot([st(1),en(1)],[st(2),en(2)],'color','black')
end

disp('x length')
disp(max(data(:,3)) - min(data(:,3)))
disp('y length')
disp(max(data(:,4)) - min(data(:,4)))
