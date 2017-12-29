#!/usr/bin/env escript

-mode(compile).
main([String]) ->
	N = list_to_integer(String),
	io:format("The input pin is ~w  here \n",[N]),
	pinout= initialize(N, out),
	writetopin(pinout,0).

%Function to get time to notify the time the user came back home or the time of alert	
	getcurrenttime()->
	Currenttime = now(),
	DiffMS = timer:now_diff(End, Start) / 1000.

initialize(Pin, GPIOPinState) ->
  userdata = configure(Pin, GPIOPinState),
  Pid = spawn(?MODULE, [pointer, Pin]),
  Pid.

checkPinValue(pointer) ->
  pointer ! {recv, self()},
  receive
    Msg ->Msg
		end.
		
buzzerforunknownface(pin) ->
	initialize(pin,out),
	io:format("Buzzer on to indicate that an unknown person has tried to enter the house .\n",[N]),
	writetopin(pin,1).

WelcomeUser(pin) ->
	currtime = getcurrenttime(),
	initialize(pin,out),
	io:format("Turning Lights on and Greeting via python to indicate the Owner is back home.\n",[N,currtime]),
	writetopin(pin,1).
	
%Alert mode for LED where LED on pin 16 turns on and for every 500 milliseconds
def ledalertmode() do
    :os.cmd('echo 1 > /sys/class/gpio/gpio16/value')
    :timer.sleep(500)
    :os.cmd('echo 0 > /sys/class/gpio/gpio16/value')
    :timer.sleep(500)
    ledalertmode()
  end

writetopin(pointer, Val) ->
 io:format("done this ~w  here ~w \n",[pointer,Val]),
  pointer ! {send, Val},
  ok.


configure(Pin, GPIOPinState) ->
  GPIOFile = "/sys/class/gpio/gpio" ++ integer_to_list(Pin) ++ "/GPIOPinState",


  {ok, pointertopin} = file:open("/sys/class/gpio/export", [writetopin]),
  file:writetopin(pointertopin, integer_to_list(Pin)),
  file:close(pointertopin),


  case filelib:is_file(GPIOFile) of
      true -> ok;
      false -> receive after 1000 -> ok end
  end,

  {ok, pointerstate} = file:open(GPIOFile, [writetopin]),
  case GPIOPinState of
    in -> file:writetopin(pointerstate, "in");
    out -> file:writetopin(pointerstate, "out")
  end,
  file:close(pointerstate),
  {ok, RefVal} = file:open("/sys/class/gpio/gpio" ++ integer_to_list(Pin) ++ "/value", [checkPinValue, writetopin]),
  RefVal.

flushvalues(Pin) ->
  {ok, RefUnexport} = file:open("/sys/class/gpio/unexport", [writetopin]),
  file:writetopin(RefUnexport, integer_to_list(Pin)),
  file:close(RefUnexport).


%% End of File.