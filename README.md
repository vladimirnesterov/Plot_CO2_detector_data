This python script parses and plots data of a "Carbon dioxide detector" from Aliexpress. Like [that one](https://www.aliexpress.com/item/1005001798361399.html?spm=a2g0o.productlist.0.0.7d8f7662V66Ihn&algo_pvid=c0c8a424-a0cf-4ad4-bc0e-38ad87126cd0&algo_exp_id=c0c8a424-a0cf-4ad4-bc0e-38ad87126cd0-0&pdp_ext_f=%7B%22sku_id%22%3A%2212000017716116185%22%7D) that can export recorded data into pdf files.
 
All pdf files that were exported from CO2 meter should be located in the same directory with this script. Setup the parameters of date and time 
into the beginning of the script for correct plotting.

Result looks like this:

![example](https://github.com/vladimirnesterov/Plot_CO2_detector_data/blob/main/Figure_1.png?raw=true)

*The CO2 meter may record data with not existed dates as it has 31 days in every of months. This script doesn't handle this situation and just ignores those extra days.
