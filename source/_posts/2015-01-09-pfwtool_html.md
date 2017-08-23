---
layout: post
title:  "Pentax Firmware Decrypting in the Web"
date:   2015-01-09 23:40:00
categories: hacking
tags:
- hacking
- webapps
---
A couple of years ago, I purchased my first DSLR: the Pentax K-30. Photography has been my hobby ever since, and I'm always looking for cool new things to push my camera further. The one thing that I really miss from my previous Canon point-and-shoot is unsurprisingly, the [Canon Hack Development Kit (CHDK)][chdk]. Luckily, most of the features that make it so useful, such as RAW image capture, live histogram, and the intervalometer are already present in the K-30. I'm not missing out on much.

But I can't resist the urge to fantasize over a programmable DSLR. So when *Pentax Forums* user *Shodan* announced he had started working on the [***Pentax** Hack Development Kit (PHDK)*][phdk], I knew I had to be a part of it.

The first step to hacking the firmware is decrypting it. *Svenpeter* made a tool called [pfwtool][pfwtool] which does an excellent job of decrypting the firmware. However, I was curious as to seeing if that functionality could be done via HTML5. My favourite file host, [MEGA](http://mega.co.nz) uses JavaScript for on-the-fly decryption, so why couldn't I? As it turns out, it was a lot easier than I thought it would be.

The web app is based off of svenpeter's awesome code. I ported it all to JavaScript and built a simple GUI that let me leverage the new file API in HTML5 to decrypt the file and spit it back out **without** uploading it. That's right -- everything happens client side. It's really nifty and if you're interested in seeing how it works, feel free to examine the [GitHub][ghd] repository.

Follow these simple steps to give it a try:

1. [Download](http://www.ricoh-imaging.co.jp/english/support/digital/firmware/k30v105.zip) the Pentax K-30 firmware (v 1.05) from Ricoh-Imaging.
2. Open the [Pentax Firmware Decrypter](/projects/pfwtool_html) in Google Chrome. Other browsers may have problems.
3. Drag the firmware file named **fwdc215b.bin** into the web page.
4. In a couple seconds, you will have a file appear in your downloads folder named **decrypted-fwdc215b.bin**.
5. Verify that it has the md5 checksum of **0afe2524251009b97639316edfe1c410**.

**That's it! Have fun with the PHDK**

[ghd]: http://github.com/MooseV2/pfwtool_html
[pfwtool]:http://github.com/svenpeter42/pfwtool
[phdk]:http://www.pentaxforums.com/forums/6-pentax-dslr-discussion/250555-resurrecting-pentax-firmware-hacking.html
[chdk]:http://chdk.wikia.com/wiki/CHDK
