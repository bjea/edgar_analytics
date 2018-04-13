To run this program, Python 3.X is required, please clone this repo then `cd edgar_analytics`, and run the shell script
named `run.sh`, e.g., `bash run.sh`.

* Approach: brute force, thus it may not be scalable.

* Tests:

** test_2: test that the program can handle an input file with an empty line or a line with only newline character ('\n'),
that it can handle some date difference and calculate duration of time with date difference (but the duration of
Line 11, 101.81.133.jja,2017-06-30 23:59:58,2017-07-01 00:00:00,4,2, of output file was incorrect, which should be 3,
not 6).

** test_3: test if the program can handle the possible maximum inactivity_period, i.e. 86400 secs; the duration of
Line 7, 107.23.85.jfd,2017-07-04 00:00:04,2017-07-07 00:00:00,86399,4, of output file was incorrect, which should be
259197, not 86399.

Therefore, there is something wrong with the way i calculate the duration, and my program cannot handle a time span of
multiple days.  However, i am too tired and need to go to bed....

