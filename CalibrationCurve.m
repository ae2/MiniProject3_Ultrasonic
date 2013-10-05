data = csvread('Calibration.csv',1,0);

fit = polyfit(data(:,2),data(:,1), 1);

hold on
plot([data(1,2), data(end,2)], [polyval(fit,data(1,2)),polyval(fit,data(end,2))],'k-','LineWidth',3)
plot(data(:,2),data(:,1),'o','markers',10,'LineWidth',3)

legend(sprintf('Linear Regression \t %fx + %f',[fit(1),fit(2)]),'Data','location','NW')

title('Calibration Curve for Ultrasonic Sensor','fontsize', 30)
xlabel('Time of Flight (Ticks)','fontsize', 24)
ylabel('Distance (cm)','fontsize', 24)
set(gca,'FontSize',20)