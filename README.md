# pyShiftTools
Contains scripts that interact with Staff API's Shift endpoints.

## SplitShifts.py
This script will call Staff Api to retireve a list of "Open" punches, then iterates through the list to conditionally split raw time punches, according to the defined payroll cutover.

### Script Arguments
All script arguments should be called with an "=" sign.

*companyid*  - Required. Unique Identifier of the company associated with your requests. <br />
*siteid*  - Optional. When this argument is omitted, ALL sites within the provided company will be processed, if they have a "type" value of 'Production'. When a script argument is provided, the script will execute only for the provided site.<br />
*keyid* - Required. Integrator Identifier value.<br />
*secret* - Required. Secret Key associated with the Integrator.<br />
*environment* - Required. Values of 'production','uat' & 'qa' are valid.<br />


### Script Execution Details
Step 1: By default, get a list of sites within a company marked with 'type' value reflecting a Production site, unless a specific "id" value is passed, which replaces the array with a single site regardless of 'type'.<br />
 This overriding behavior could be applied to internal and customer labs.<br />
Step 2: Get the Payroll Cutover time value from Xenial Data Management (Business Rules - Payroll). This value will be used to bookend shifts.<br />
Step 3: Get a list of Punches with Clock Statuses of "Clocked In" and "On Break".<br />
Step 4: Iterate through the array of objects included in the response.<br />
Step 4a: If number_of_breaks is 0, end the shift with a Clock Out time equivalent to the Payroll Cutover time. Create a new shift with a 'Clock In' value equivalent to the Payroll Cutover Time and a 'Clock Out' value of NULL.<br />
Step 4b: If number_of_breaks is > 0, end the shift with a Clock Out time equivalent to the Payroll Cutover time. End the Break without a 'Clock Out' value, setting its time to (1) Second prior to the Clock Out for the overall shift.Create a new shift with a 'Clock In' value equivalent to the Payroll Cutover Time and a 'Clock Out' value of NULL, with a break beginning at the Payroll Cutover Time. The break end time is likewise NULL.<br />

### Logging
A log file will be created in the current directory, suffixed with the date.
