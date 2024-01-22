# l1pcap - Radio Frequency - ? points - ? solves

On relaxing afternoons, I sometimes like to sit around and just watch the waves -- radio waves, that is!

On one particular afternoon as I was listening at a center frequency of 433 MHz, sampling at 2 Msps with a bandwidth of 2 MHz, I picked up some RF from my neighbor. Every time a signal was transmitted, I saw that some stuff happened around their house, so I think that this is some kind of a home remote control system.

I captured the signals and tried replaying them, but it didn't work! There must be some kind of a mechanism to prevent replay attacks. If you can complete the analysis of the captured signals, then we should be able to transmit our own commands to make their house go berserk!

```
Signal 1(a) and 1(b):
<message: "GARAGE OPEN"> .. <message: "GARAGE CLOSE">

Signal 2(a) and 2(b):
<message: "ROOM 1 LIGHTS ENABLE"> .. <message: "ROOM 1 LIGHTS DISABLE">

Signal 3(a) and 3(b):
<message: "ROOM 2 LIGHTS ENABLE"> .. <message: "ROOM 2 LIGHTS DISABLE">

Signal 4(a) and 4(b):
<message: "FRONT SPRINKLERS ENABLE"> .. <message: "FRONT SPRINKLERS DISABLE">

Signal 5(a) and 5(b):
<message: unknown> .. <message: unknown>

Signal 6(a) and 6(b):
<message: unknown> .. <message: unknown>

Signal 7(a):
<message: unknown>
```

These signals were transmitted in sequential order, so 1(a) was transmitted first, 1(b) second, 2(a) third, etc.

Kids these days are so used to using Wireshark to analyze wireless traffic, but what if the wireless traffic you're trying to analyze isn't Wi-Fi-based?

By: skat

Handout:
- https://cdn.2024.irisc.tf/l1pcap.tar.gz

Flag: `irisctf{fsk_p4ck3ts_and_wh1t3n1ng_w3re_n0_m4tch_4_u}`
