# tooltip


2025-05-14 07:27
[[header |Main]] | [[_Idx-AA_Journal|_Idx-AA_Journal]]

This does not show. for testing only
CB| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | (https://yahoo.com)   |
| Cell 3   | [here](https://www.google.com)   |
| Cell 3   | https://www.cnn.com |
image-align-{alignment} mobile-align-center mobile-default-size

<div style="break-after: page;"></div><br>
## Elevating Understanding
![[ElevatingUnderstanding.svg]]<br><p style="color: #f09e5a;"><span class="highlight-text">tooltip tooltip</span></p>

<div>
Position    Parameter	  Purpose	                                Example values<br>
1           T →         data-top (default: 5.5vh)<br>
2           L →         data-left (default: 6.5vw)<br>
3           BG →        data-bottom-gap (default: 0vh)<br>
4           H →         data-height<br>
5           W →         data-width<br>
6           MH →        data-maxheight<br>
7           MW →        data-maxwidth<br>
8           loc →       data-position (default: "bottom-page")<br>
9            tloc →      data-textalign (default: "left")<br>
[ Top | Left | Bot_GAP | Height | Width | Maxheight | MaxWidth | LOC | TLOC ]<br>

same as  <ttt-LEXTIP=":[floatright]default", ":[  |  |  | |  | | | center-width | left ]Some information here">,<br>

Only tip text (no parameters) <ttt-LEXTIP=":[floatright]Info", ":[ ]Some information here"><br>
Set height and width <ttt-LEXTIP=":[floatright]Image", ":[ | | |30%| 84% ]Click to view"><br>
Set max‑height and max‑width only <ttt-LEXTIP=":[floatcenter]Centered", ":[|||||| |center-both|center]Perfectly centered tooltip"><br>
Combine multiple parameters <ttt-LEXTIP=":[floatright]Flex", ":[|||200px|60vw|250px|80vw|center-width|right]Dynamic tooltip"><br>
No float marker (trigger stays inline) <ttt-LEXTIP="Info", ":[|||300px||| |bottom-page|center]Tooltip info">

Custom positionioned tooltip <ttt-LEXTIP=":[floatright]Info", ":[10vh|20vw|2vh|200px|400px|||center-width|center]Custom positioned tooltip">
<ttt-LEXTIP="Word", ":[]Tip All Defaults">

have a word that we want to stick to the right margin. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est srinivas <ttt-LEXTIP=":[floatright]t-FH-34W-TL", ":[  |  |  | 90% | 75% | 94% | 90% | center-width | left ]FullPage with tip text left justified - t-FH-34W-TL"><br>

<ttt-LEXTIP="test-this", ":[5.5vh|9vw| ||| | |center-width|left]tt-FP-TL<br>Full page centered, text left">
<ttt-LEXTIP="tt-FP-TL", ":[5.5vh|9vw| |90%|60%| | |center-width|left]tt-FP-TL<br>Full page, 60% wide, centered, text left"> <ttt-LEXTIP=":[floatright]tt-FP-TC", ":[5.5vh|9vw| | 90%|60%| | |center-width|center]tt-FP-TC<br>Full page, 60% wide, centered, text left"><br>
<ttt-LEXTIP="tt-FH-34W-TL", ":[5.5vh|9vw| |90%|75%| ||center-width|left]tt-FP-TL<br>Full page, 3/4 wide, centered, text left"><ttt-LEXTIP=":[floatright]tt-34H-34W-TL", ":[5.5vh|9vw| |90%|75%| |75%|center-width|left]tt-FP-TL<br>3/4 page, 60% wide, centered, text left"><br>
<ttt-LEXTIP="tt-1/4H-FW-TL", ":[5.5vh|9vw| |22.5%|84%| | |center-width|left]tt-14H-FW-TL<br>FullWidth Top, 1/4 height - tt-14H-FW-TL-TOP"><ttt-LEXTIP=":[floatright]tt-14H-34W-TL", ":[5.5vh|9vw| |22.5%|84%| | |bottom-page|left]tt-14H-34W-TL<br>"FullWidth Bottom, 1/4 height - tt-14H-FW-TL-BOT"><br>
<ttt-LEXTIP="tt-13H-FW-TL-TOP", ":[5.5vh|9vw| |30%|84%| | |center-width|left]tt-FP-TL-TOP<br>FullWidth Top, 1/3 height - tt-14H-FW-TL-TOP"><ttt-LEXTIP=":[floatright]tt-13H-FW-TL-BOT", ":[5.5vh|9vw| |30%|84%| | |bottom-page|left]ttt-13H-FW-TL-BOT<br>"FullWidth Bottom, 1/3 height - tt-14H-FW-TL-BOT"><br>
<ttt-LEXTIP="tt-12H-FW-TL-TOP", ":[5.5vh|9vw| |45%|84%| | |center-width|left]tt-12H-FW-TL-TOP<br>FullWidth Top, 1/2 height - ttt-12H-FW-TL-TOP"><ttt-LEXTIP=":[floatright]tt-12H-FW-TL-CTR1", ":[5.5vh|9vw| |45%|84%| | |center-both|left]ttt-14H-FW-TL-CTR<br>"FullWidth Center, 1/2 height - tt-12H-FW-TL-CTR"><ttt-LEXTIP=":[floatright]tt-12H-FW-TL-BOT", ":[5.5vh|9vw| |45%|84%| | |bottom-page|left]ttt-14H-FW-TL-BOT<br>"FullWidth Bottom, 1/2 height - tt-12H-FW-TL-BOT"><br>


FLEX TOP The popup’s content may be scrollable but the bottom of the scrollable area is not reachable because of the way the popup is positioned – For example, if the popup is positioned very low on the page, the bottom part might be outside the viewport. But with top: 5.5vh and height: 22.5vh, its bottom is at 28vh, well inside the viewport. So that shouldn’t happen.A max-height from a parent or from the #tooltip rule with !important could interfere – In your CSS, #tooltip also has overflow-y: auto and no max-height, so it’s fine.<br> Another thing: the #tooltip also has overflow-y: auto, but that might be overridden by the inline style from the trigger? No, the inline style sets only height and max-height, not overflow.I'd suggest the user inspects the popup element in the browser's Elements panel after clicking, and look at the computed styles for height, overflow-y, and see if there is any other rule interfering. Also, check if the scrollbar is present. If the scrollbar is present but dragging doesn't scroll to the bottom, perhaps the scroll position is limited because the content's bottom is being cut off by something like a bottom property? The tooltip has a fixed position; if top is set <ttt-LEXTIP="tt-1/4H-FW-TL", ":[5.5vh|9vw| |22.5vh|50vw| | |center-width|left]tt-14H-FW-TL FullWidth Top, 1/4 height - tt-14H-FW-TL-TOP - iInspect the popup – Right‑click on the tooltip when it appears, choose “Inspect”, and look Check its computed height, max-height, and overflow-y. Ensure that the inline height is present and that overflow-y is auto. Also check if the scrollbar is visible. If the scrollbar is present but you can’t scroll to the bottom, it might be because the content is actually not taller than the container. Verify the content length. If it is taller, try adding overflow-y: scroll (instead of auto) to force a scrollbar. You can do this by modifying the script to set overflow-y from a data-overflow attribute, or simply rely on the CSS class which already has auto. If the scrollbar is not showing, maybe the content height is less than the container.The CSS max-height from the class is still limiting the actual height – even though you set height: 22.5%, if <br> the class’s max-height is smaller, it will override the height. In your CSS, has 22.75vh. Since 22.5% of viewport height is about 22.5vh (slightly smaller), the max-height from the class is actually larger, so it doesn’t restrict. So that’s not the problem. The overflow-y: auto may be missing or overridden – The popup gets the class  which sets overflow-y: auto. Inline styles do not set overflow, so it should be present. Check in the browser that the popup’s computed overflow-y is auto. The popup’s content may be scrollable but the bottom of the scrollable area is not reachable because of the way the popup is positioned – For example, if the popup is positioned very low on the page, the bottom part might be outside the viewport. But with top: 5.5vh and height: 22.5vh, its bottom is at 28vh, well inside the viewport. So that shouldn’t happen.A max-height from a parent or from the #tooltip rule with !important could interfere – In your CSS, #tooltip also has overflow-y: auto and no max-height, so it’s fine.<br> Another thing: the #tooltip also has overflow-y: auto, but that might be overridden by the inline style from the trigger? No, the inline style sets only height and max-height, not overflow.I'd suggest the user inspects the popup element in the browser's Elements panel after clicking, and look at the computed styles for height, overflow-y, and see if there is any other rule interfering. Also, check if the scrollbar is present. If the scrollbar is present but dragging doesn't scroll to the bottom, perhaps the scroll position is limited because the content's bottom is being cut off by something like a bottom property? The tooltip has a fixed position; if top is set and the height is fixed, the content should be scrollable.Given the time, I'll provide a concise answer: The tooltip height is set to 22.5% of the viewport, but if the content is longer, you should be able to scroll. If scrolling doesn't reach the bottom, inspect the popup's computed height and overflow. Ensure the max-height from the CSS class isn't smaller than 22.5vh. Also, verify that the popup's bottom is not set to something that prevents scrolling. If you still can't scroll, add overflow-y: auto !important to the inline style via data-maxheight or modify the script to set overflow-y as well. But the simpler solution is to set the height to auto (remove the height parameter) and use max-height to limit, which is the typical approach."> <br>


FLEX CENTER from a parent or from the #tooltip rule with !important could interfere – In your CSS, #tooltip also has overflow-y: auto and no max-height, so it’s fine.<br> Another thing: the #tooltip also has overflow-y: auto, but that might be overridden by the inline style from the trigger? No, the inline style sets only height and max-height, not overflow.I'd suggest the user inspects the popup element in the browser's Elements panel after clicking, and look at the computed styles for height, overflow-y, and see if there is any other rule interfering. Also, check if the scrollbar is present. If the scrollbar is present but dragging doesn't scroll to the bottom, perhaps the scroll position is limited because the content's bottom is being cut off by something like a bottom property? The tooltip has a fixed position; if top is set <ttt-LEXTIP="tt-1/4H-FW-TL-CTR", ":[5.5vh|9vw| |22.5vh|50vw| | |center-both|left]tt-14H-FW-TL FullWidth Top, 1/4 height - tt-14H-FW-TL-CTR- - iInspect the popup – Right‑click on the tooltip when it appears, choose “Inspect”, and look Check its computed height, max-height, and overflow-y. Ensure that the inline height is present and that overflow-y is auto. Also check if the scrollbar is visible. If the scrollbar is present but you can’t scroll to the bottom, it might be because the content is actually not taller than the container. Verify the content length. If it is taller, try adding overflow-y: scroll (instead of auto) to force a scrollbar. You can do this by modifying the script to set overflow-y from a data-overflow attribute, or simply rely on the CSS class which already has auto. If the scrollbar is not showing, maybe the content height is less than the container.The CSS max-height from the class is still limiting the actual height – even though you set height: 22.5%, if <br> the class’s max-height is smaller, it will override the height. In your CSS, has 22.75vh. Since 22.5% of viewport height is about 22.5vh (slightly smaller), the max-height from the class is actually larger, so it doesn’t restrict. So that’s not the problem. The overflow-y: auto may be missing or overridden – The popup gets the class  which sets overflow-y: auto. Inline styles do not set overflow, so it should be present. Check in the browser that the popup’s computed overflow-y is auto. The popup’s content may be scrollable but the bottom of the scrollable area is not reachable because of the way the popup is positioned – For example, if the popup is positioned very low on the page, the bottom part might be outside the viewport. But with top: 5.5vh and height: 22.5vh, its bottom is at 28vh, well inside the viewport. So that shouldn’t happen.A max-height from a parent or from the #tooltip rule with !important could interfere – In your CSS, #tooltip also has overflow-y: auto and no max-height, so it’s fine.<br> Another thing: the #tooltip also has overflow-y: auto, but that might be overridden by the inline style from the trigger? No, the inline style sets only height and max-height, not overflow.I'd suggest the user inspects the popup element in the browser's Elements panel after clicking, and look at the computed styles for height, overflow-y, and see if there is any other rule interfering. Also, check if the scrollbar is present. If the scrollbar is present but dragging doesn't scroll to the bottom, perhaps the scroll position is limited because the content's bottom is being cut off by something like a bottom property? The tooltip has a fixed position; if top is set and the height is fixed, the content should be scrollable.Given the time, I'll provide a concise answer: The tooltip height is set to 22.5% of the viewport, but if the content is longer, you should be able to scroll. If scrolling doesn't reach the bottom, inspect the popup's computed height and overflow. Ensure the max-height from the CSS class isn't smaller than 22.5vh. Also, verify that the popup's bottom is not set to something that prevents scrolling. If you still can't scroll, add overflow-y: auto !important to the inline style via data-maxheight or modify the script to set overflow-y as well. But the simpler solution is to set the height to auto (remove the height parameter) and use max-height to limit, which is the typical approach."> 



FLEX BOTTOM CENTER if the scrollbar is present. If the scrollbar is present but dragging doesn't scroll to the bottom, perhaps the scroll position is limited because the content's bottom is being cut off by something like a bottom property? The tooltip has a fixed position; if top is set and the height is fixed, the content should be scrollable.Given the time, I'll provide a concise answer: The tooltip height is set to 22.5% of the viewport, but if the content is longer, you should be able to scroll. If scrolling doesn't reach the bottom, inspect the popup's computed height and overflow.<ttt-LEXTIP="tt-1/4H-FW-TL-BOT", ":[5.5vh|9vw| |22.5vh|50vw| | |bottom-center|left]tt-14H-FW-TL-BOTCTR FullWidth Top, 1/4 height - tt-14H-FW-TL-BOTCTR - in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. <br><br> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. <br><br> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. <br><br> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<br><br> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. <br><br> Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."> 


in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. abcd

<ttt-LEXTIP=":[floatleft]CW L", ":[ @| | | | | | | | left]Your tooltip text here"><br>
<ttt-LEXTIP=":[floatcenter]CW M", ":[ @| | | | | | | | left]Your tooltip text here"><br>
<ttt-LEXTIP=":[floatright]CW R", ":[ @| | | | | | | | left]Your tooltip text here"><br>

///<ttt-LEXTIP=":[floatxxxt]word", ":[ Top | left | Bottom-gap | Height | Width | MaxHeight| Maxwidth | LOC | TLOC ]tip"> 
<ttt-LEXTIP=":[floatleft]TL", ":[ 5.5vh | 0px | 0 | 160px | 150px | | | absolute | center ]📌 Top Left Corner"><br>
<ttt-LEXTIP=":[floatcenter]TC", ":[ 0px | calc(50% - 75px) | 0 | 160px | 150px | | | absolute | center ]📌  Top center">
<ttt-LEXTIP=":[floatcenter]TC", ":[0px | center | 0 | 160px | 150px | | | fixed | center]📌 Top center">
<ttt-LEXTIP=":[floatcenter]LC", ":[center | 0 | 0 | 160px | 150px | | | fixed | center]📌 left center">
<ttt-LEXTIP=":[floatcenter]CC", ":[center | center | 0 | 160px | 150px | | | fixed | center]📌 Middle of page with top=center left=center">
<ttt-LEXTIP=":[floatcenter]CC", ":[ | | 0 | 160px | 150px | | | center-both | center]📌 Middle of Page with position= center-both">
<ttt-LEXTIP=":[floatcenter]TR", ":[ 0px | calc(100% - 150px - 42px) | 0 | 160px | 150px | | | absolute | center ]📌 Top right Corner">
<ttt-LEXTIP=":[floatcenter]RC", ":[ center| calc(100% - 150px - 42px) | 0 | 160px | 150px | | | fixed | center ]📌 Right center">
<ttt-LEXTIP=":[floatright]BL", ":[ |  | 0 | 160px | 150px | | | bottom-left | center ]📌 btoom left"><br>
<ttt-LEXTIP=":[floatright]BC", ":[ |  | 0 | 160px | 150px | | | bottom-center | center ]📌 btoom left"><br>
<ttt-LEXTIP=":[floatright]BR", ":[ |  | 0 | 160px | 150px | | | bottom-right | center ]📌 btoom left">
</div>



<p style="margin-right:8%; text-align: right; font-style: italic;">
<span class="tooltip-trigger right-justified" 
  data-top="center"  data-left="center"     data-height="90%"   data-width="95%" 
  data-textalign="center"             data-tiptext="📱 Fullscreen Tooltip">
  Fullscreen </span>
</p>

<p style="text-align: center; font-style: italic;">
  <span class="tooltip-trigger"
    data-top="calc(100% - 60vh - 60px)" data-left="100px"   data-height="60vh"  data-width="30vw"   data-textalign="left"
    data-tiptext="Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: 
    Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 
    5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth animations.
    <br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>
    Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved! 
    Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing 
    elit.<br>Line 3: Sed do eiusmod tempor ling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
    animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
    tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
    Smooth animations preserved! Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>
    Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempoincididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>
    Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
    animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
    tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
    Smooth animations preserved!">
    Scrollable - left </span>
</p>

<p style="text-align: center; font-style: italic;">
  <span class="tooltip-trigger"
    data-top="calc(100% - 60vh - 60px)"     data-left="100px"   data-height="60vh"  data-width="30vw"   data-textalign="center"
    data-tiptext="Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: 
    Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 
    5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth animations.
    <br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>
    Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved! 
    Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing 
    elit.<br>Line 3: Sed do eiusmod tempor ling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
    animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
    tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
    Smooth animations preserved! Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>
    Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempoincididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>
    Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
    animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
    tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
    Smooth animations preserved!">
    Scrollable - center </span>
</p>

<p style="text-align: center; font-style: italic;">
<span class="tooltip-trigger center-justified"
  data-top="calc(100% - 60vh - 60px)"     data-left="100px"   data-height="60vh"  data-width="30vw"   data-textalign="right"
  data-tiptext="Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: 
  Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 
  5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth animations.
  <br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempor incididunt.<br>
  Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved! 
  Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing 
  elit.<br>Line 3: Sed do eiusmod tempor ling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
  animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
  tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
  Smooth animations preserved! Long scrollable content with smooth animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>
  Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod tempoincididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>
  Line 5: Very long content forces scrolling.<br>Line 6: Smooth animations preserved!<br>Long scrollable content with smooth 
  animations.<br><br>Line 1: Lorem ipsum dolor sit amet.<br>Line 2: Consectetur adipiscing elit.<br>Line 3: Sed do eiusmod 
  tempor incididunt.<br>Line 4: Ut labore et dolore magna aliqua.<br>Line 5: Very long content forces scrolling.<br>Line 6: 
  Smooth animations preserved!">
  Scrollable - right </span>
</p>

<p style="text-align: center; font-style: bold;"> ~***~ </p>

