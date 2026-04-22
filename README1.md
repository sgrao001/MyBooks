# README1
README1

                                

_HTML STYLING_____________________________________________________________________________________________________________________________

<p style="
    font-family: Arial, sans-serif;
    font-style: italic;
    font-size: 18px;
    color: darkgreen;
    background-color: #f0f0f0;
    border: 2px dashed green;
    padding: 12px;
    margin: 20px;
    line-height: 1.6;
    text-transform: capitalize;
    letter-spacing: 1px;
    text-shadow: 1px 1px 2px lightgray;
    box-shadow: 3px 3px 5px #ccc;
    Text-align: center;
    cursor: pointer;
    text-indent: 40px;
">
    This paragraph demonstrates various inline styling properties including text indent, 
    borders, padding, margin, line height, and more. The first line of this paragraph 
    begins with a 40px indent..
</p>

- Underline with                <u> xxxx </u> inside the p-tag
- vHighlight with               <span class="highlight-text">This is highlighted text</span> inside the p-tag
- Borders: Add borders 

  around the paragraph          border: 1px solid black;  or any style/color.
                            
- Padding and margin:           padding: 10px 
  Control spacing padding       argin: 10px;
  inside  & margin outside      

- Line height: Adjust s         line-height: 1.5; 
  pacing between lines with  
                            
- Text transform: Change        text-transform: uppercase;  or  capitalize .
  case with  
                            
- Letter spacing and            Use letter-spacing:   and  word-spacing  to adjust 
  word spacing:                 spacing between letters or words.
                            
- Text shadow:                  Add shadow to text with  text-shadow: 2px 2px 3px gray; .
- Opacity:                      Make paragraph partially transparent, e.g.  opacity: 0.7; .
- Box shadow:                   Apply shadow around the paragraph box with  box-shadow .
- Cursor:                       Change mouse cursor style on hover with  cursor: pointer; .
- White-space handling:         Control whether to collapse whitespace or wrap with  white-space .

  <p class="inline">            Display inline - flows with text, no new line.</p>
  <span>--</span>               This text is on the same line as the inline paragraph.</span>
  <p class="none">              You should not see this paragraph (display: none).</p>

                                <span> element can be placed inside a <p> tag. A <span> 
                                element can have all the inline styling that a  <p>  element 
                                can have. Some CSS properties related to block layout (like  
                                margin-top , margin-bottom , or  width ,  height ) may not 
                                behave as expected on a  <span>  because it 
                                doesn’t create a block box by default. For purely   
                                text-related styles—such as  font-family ,  
                                font-size ,  font-weight  (bold),  font-style  (italic),    
                                text-decoration  (underline), color , background-color ,  
                                text-align  (when applied to a block   container parent),  
                                letter-spacing ,   line-height , text-shadow ,  opacity , 
                                and many more— <span> handles them just like  <p>  does.

This is line one.<br><br><br>   This is line two after three line breaks blanks.
  
_BULLETS___________________________________________________________________________________________________________________________________

  &bull;                        First point in a bulleted line<br>
  &bull;                        Second bullet with more information<br>
  &bull;                        Third item continues in normal paragraph flow

Adds three bullet points as plain-text symbols ( -  ). Each line is broken using  <br>  for 
line breaks

_URL LINKS_________________________________________________________________________________________________________________________________

This is a paragraph with a 
  <a href="https://www.example.com">link to Example.com</a> 
  inside it.
  Go to the <a href="#section2">second section</a> of this page.
  Go to the <a href="#section2">second section</a> of this page. Where there is a <p id="section2"> S
  omewhere in the document. 

  In the .md file do this...
  [Image Src...](https://www.wikiart.org/en/pablo-picasso/friendship-1908)

  for reference / image  links use 
<p style="font-size: 0.4em;">[Image Src...](url)</p>

_IMAGE OPTIONS_____________________________________________________________________________________________________________________________

Image Syntax Options: ![[ filename | description | size | alignment ]]
1. ![[image]]                                   - Just filename
2. ![[image | My description]]                  - Filename + description
3. ![[image | | 300px]]                         - Filename + size (no description)
4. ![[image | | 50%]]                           - Filename + percentage size
5. ![[image | | 400x300]]                       - Filename + dimensions
6. ![[image | | 400]]                           - Filename + auto-px size
7. ![[image | | | center]]                      - Filename + alignment only
8. ![[image | | | left]]                        - Filename + left alignment
9. ![[image | | | right]]                       - Filename + right alignment
10. ![[image | Description | 300px]]            - Filename + description + size
11. ![[image | Description | 50%]]              - Filename + description + percentage
12. ![[image | Description | 400x300]]          - Filename + description + dimensions
13. ![[image | Description | 400]]              - Filename + description + auto-px
14. ![[image | Description | | center]]         - Filename + description + alignment
15. ![[image | Description | | left]]           - Filename + description + left align
16. ![[image | Description | | right]]          - Filename + description + right align
17. ![[image | | 300px | center]]               - Filename + size + alignment
18. ![[image | | 50% | left]]                   - Filename + percentage + left align
19. ![[image | | 400x300 | right]]              - Filename + dimensions + right align
20. ![[image | | 400 | center]]                 - Filename + auto-px + alignment
21. ![[image | Description | 300px | center]]   - All parameters: centered
22. ![[image | Description | 300px | left]]     - All parameters: left aligned
23. ![[image | Description | 300px | right]]    - All parameters: right aligned
24. ![[image | Description | 50% | center]]     - All: percentage + centered
25. ![[image | Description | 400x300 | left]]   - All: dimensions + left
26. ![[image | Description | 400x300 | right]]  - All: dimensions + right
Size Options:
* 300px - Fixed pixels
* 50% - Percentage width
* 400x300 - Width × Height
* 400 - Auto-convert to pixels
Alignment Options:
* center - Centered
* left - Left aligned, text wraps right
* right - Right aligned, text wraps left
text pop-up when hover or click
All parameters are optional except the filename! Use empty | placeholders to skip parameters.

_REPLACEMENTS_____________________________________________________________________________________________________________________________
  ///                         Comment line - Delete to the end of the line
  From //* to *//             comment parapgh - Delete Between 
  **text** or __text__        Remove BOLD
  ==text==                    Remove Highlight
  *text* or _text_            Remove Itlalics
  <u>text</u>                 Remove bullets
  <em>text</em>               Remove Emphasis

_PAGE HANDLING_____________________________________________________________________________________________________________________________

  Anything above this is ignored.This is goels on top of the file
  <STARTPAGE> / <NEWPAGE>
  <CHAPTER="1"> 
  <IMAGE="xxx">
  <TITLE="xxx"> 

    Paragraphs............

  <PAGE END MARKER="xxx"> 
  <ENDPAGE> / <NEWPAGE>

_General Items_____________________________________________________________________________________________________________________________
Item                                                Description - Label and URL canbe single, double quoted or none. COmmas and pipes work
___________________________________________________________________________________________________________________________________________
[text] (URL)                <a href="url>test</a>                                 (HTML LINK)
<STARTPAGE>, <NEWPAGE>      <div style="break-after: page;"></div><br>
<ENDPAGE>                   <div style="break-after: page;"></div><br>
<PAGEDIVIDER>               <hr style="height: 1.2px; background-color: var(--text-color); opacity: 0.3; border: none;">

<IMAGE=filename>             Converts ![[filename]] (xxx is a tring with | separated image attributes - see below)
<TITLE="xxx">               <p style="color: #f09e5a;"><span class="highlight-text">xxx</span></p>xxx</span></p>
<ClipBookMark>              <DPosition=':[ both | ] <a href="..." onclick="..."><span class="glassbtn">🔖</span></a> '>
<clipBookMark="xxx">        <DPosition=':[ both | ] <a href="..." onclick="..."><span class="glassbtn">🔖</span></a> <span class="glassbtnlbl">Copy link</span>'>
<IMAGEATR="xxx">              <p style="text-align: center; font-size: 0.4em;">[Image Src...](xxx)</p>. also allow 
<CHAPTER="xxx">             ## xxx also support 'xxx' there will be a space between ## and xxx
<IMAGE="xxx">               ![[xxx]] and also support 'xxx'
<PAGE END MARKER="xxx">     <p style="text-align: center; font-style: bold;"> xxx</p> ignore space and also support 
<FOOTER="xxx">              <p style="font-size: 0.4em;">xxx</p>                                          (Paragraph Tiny footer)

<NEXTPAGE_ICON>                                     <span class="next-page">👉</span>
<PREVPAGE_ICON>                                     <span class="prev-page">👈</span>
<ClickMe_icon>                                      <span class='glassbtn'>👆</span>

_DOUBLE QUOTES required_ _Anywhere there is are HTML tages in strings use Double quotes_
<TITLE="Label">                                     <span style="color: #f09e5a;"><span class="highlight-text">Label</span>

_DSome Styling Options_
<color="xxx">                                         <span style="color: xxx">{m.group(4)}</span>. Only works inside a SPAN, DIV or P tags
<Superscript="xxx">                                   <sup>"xxx"</sup>
<Subscript="xxx">                                     <sub>"xxx"</sub>
<bold="xxx">                                          <b>"xxx"</b>
<underline="xxx">                                     <u>"xxx"</u>
<italics="xxx">                                       <i>"xxx"</i>
<LineHeight="", "yyy">                                <span style='line-height: xxxem;'>yyy</span>

_Leave paraitalic* blank is itelas not desired_
<ParaitalicL="xxx">                                 <DPosition=':[left  |  paraitalicleft ] xxx'>
<ParaitalicC="xxx">                                 <DPosition=":[center | paraitaliccenter ] xxx">
<ParaitalicB="xxx">                                 <DPosition=":[both | paraitalicleft ] xxx">
<ParaitalicR="xxx">                                 <DPosition=":[right | paraitalicleft ] xxx">

_CLICKWORDS GIVE YOU A POPUP TEXT BOX_
_in the clickwords below put @ in either a or b, if thats what you want_
_Leave a and b blank if you want autogrowing and center-both_
_inserting a or b will remove auto growth for that parameter_
_xxx must be in double quotes_
_5 required after a and b otherwise px is assumed_
<clickwordL= a% | b% | "xxx">                         <BBL-Txt=":[floatleft]<ClickMe_icon>", ":[ | | |a%| b% | | |center-both|left]xxx">
<clickwordC= a% | b% | "xxx">                         <BBL-Txt=":[floatcenter]<ClickMe_icon>", ":[ | | |a%| b% | | |center-both|left]xxx">
<clickwordR= a% | b% | "xxx">                         <BBL-Txt=":[floatright]<ClickMe_icon>", ":[ | | |a%| b% | | |center-both|left]xxx">
<clickword0= a% | b% | "xxx">                         <BBL-Txt="<ClickMe_icon>", ":[ | | |{a}%| {b}% | | |center-both|left]xxx">

_Inline CLICKWORDS_
<ClickwordInline='Something.... <clickword0= 30 | 80 | "Tiptext1"> and something else I<clickword0= 30 | 80 | "Tiptext2"> and now I am done '>

___________________________________________________________________________________________________________________________________________

_DPosition - Indenting_____________________________________________________________________________________________________________________
_DPOSITION ALLOW INDENTING OF PARAGRAPHS_ 
_SINGLE QUOTES required_ 
_Leave glasslbl blank if italics not desired_ 
<DPosition=':LRCB[ walign | glassbtnlbl ] xxx'>  Supports both pipe and comma. 

Parameter	  Purpose	                  Allowed Values	                      Default (if empty)	    CSS Generated
___________________________________________________________________________________________________________________________________________
walign	    Sets horizontal margin    left, right, center, both             No margin rule          margin-left: ARW_SAFE_MARGIN; margin-right: ARW_SAFE_MARGIN;
            (indentation/centering)	  or empty                                                      margin-left: auto; margin-right: auto;
                                                                                                    margin-left: ARW_SAFE_MARGIN; margin-right: ARW_SAFE_MARGIN;
                                                                                                    (empty → no rule)		
lblclass    sets visual parameters                                                   .glassbtnlbl {{ color: #4fc3f7; font-size: 0.8em; font-family: sans-serif; 
                                                                                                font-weight: normal; text-decoration: none; font-style: normal;
                                                                                                text-align: left;}}   
                                                          
                                                                                    .paraindientleft {{ font-style: italic; text-align: left; }}
                                                                                    .paraindientright {{ font-style: italic; text-align: right; }}
                                                                                    .paraindientcenter {{ font-style: italic; text-align: center; }} 
___________________________________________________________________________________________________________________________________________ 

_BUBBLETEXT_______________________________________________________________________________________________________________________________
:[floatright]     – trigger floats right, with a right margin of ARW_SAFE_MARGIN.
:[floatleft]      – trigger floats left, with a left margin of ARW_SAFE_MARGIN.
:[floatcenter]    – trigger is centered (block with auto margins).
:[floatboth]      - inline 
_BubbleText & tiptext position_____________________________________________________________________________________________________________
Position    Parameter	  Purpose	                                        Default                   
___________________________________________________________________________________________________________________________________________
floatmarker
1           T →         data-top                                        5.5vh
2           L →         data-left                                       6.5vw
3           BG →        data-bottom-gap                                 0vh
4           H →         data-height                                     var(--BBLTxt-max-height) (91vh desktop)
5           W →         data-width                                      var(--BBLTxt-max-height) (91vh desktop)
6           MH →        data-maxheight                                  var(--BBLTxt-max-height) (91vh desktop)
7           MW →        data-maxwidth                                   var(--BBLTxt-max-height) (91vh desktop)
10          loc →       data-position                                  "bottom-left"
11          tloc →      data-textalign                                  "left"
_USAGE_____________________________________________________________________________________________________________________________________
_DOUBLE QUOTES required_ for WORD and TIPTEXT
<BBL-Txt=":[floatxxx]word", ":[ data-top | data-left | Bottom-gap | data-height | data-width | data-maxheight| data-maxwidth | data-position | data-textalign  ]tiptext"> 
<BBL-Txt=":[floatleft]Click word", ":[ @| | | | | | | | left]Your BubbleText text here"><br> (fullheight and full width)
Supports both Pipe and commna
___________________________________________________________________________________________________________________________________________
Attribute	          Purpose	                          Example Values (all labels are case censitive)
___________________________________________________________________________________________________________________________________________
data-position	      Defines how the BubbleText        center-height    – centers BubbleText vertically (viewport then clamped to page)
                    is positioned relative            center-width     – centers horizontally
                    to the trigger and the            center-both      – centers both axes
                    viewport/page.                    bottom-page      – places BubbleText at the bottom left of the page with a gap but uses
                                                                         Data.Left to position horizontally
                                                      bottom-left      – places BubbleText at the bottom left of the page with a gap
                                                      bottom-center    – CENTERS the  BubbleText at the bottom left of the page with a gap
                                                      bottom-right     – places BubbleText at the bottom left of the page with a gap
                                                      fixed (default)  – uses explicit top/left/bottom/right values relative to viewport
                                                                        TOP center -> data-left = center & data-position = fixed 
                                                                        Center-Center -> data-left= center, data-top=center, data-position=fixed
                                                      absolute         - The BubbleText is positioned using the top/bottom and left/right 
                                                                          values you provide (or defaults). No special layout adjustments 
                                                                          are made   
                                                                                      
_________________________________________________________________________________________________________________________________________
data-top          @             Width is forced to 50 vw (half the viewport width). Max‑height is forced to 3 em (content scrolls 
                                if longer).These dimensions are applied with !important to override any CSS classes.The BubbleText’s height 
                                is set to auto so it only grows as needed, up to the max‑height. Left if trigger center < 25 vw → BubbleText’s 
                                left edge is 5 vw from the left viewport edge. Center if trigger center between 25 vw and 75 vw → BubbleText 
                                is horizontally centered in the viewport. Right if trigger center > 75 vw → BubbleText’s right edge is 5vw 
                                from the right viewport edge.
_________________________________________________________________________________________________________________________________________
	                Sets the BubbleText’s position       
data-top          relative to the viewport or 
data-bottom       page. Can be CSS lengths 
data-left         (e.g., 10vh, 20px, 50%) or          10vh, 20px, 50%, @
data-right        the special value "@" which 
                  snaps the corresponding edge 
                  to the same edge of the 
                  trigger  element.	
                  data-left supports center
___________________________________________________________________________________________________________________________________________
data-bottom-gap	  Only used with data-position
                  ="bottom-page". Adds a gap 
                  between the BubbleText’s bottom        2vh, 10px
                  edge and the bottom of the 
                  page (or viewport).	
___________________________________________________________________________________________________________________________________________
data-animation	  Chooses the BubbleText’s               fade (default), bounce, slide, zoom
                  entrance/exit animation.	
___________________________________________________________________________________________________________________________________________
data-textalign	  Aligns the BubbleText text             left (default), center, right
                  inside the BubbleText box.	
___________________________________________________________________________________________________________________________________________
data-tiptext	    The actual BubbleText 
                  content (HTML allowed,              any string (e.g., "This is a BubbleText")
                  escaped by JavaScript).	                  
___________________________________________________________________________________________________________________________________________ 
Attribute	        Purpose	Example Values	Notes
data-width	      Explicit width of BubbleText          300px, 50vw, auto (default)	      Overrides any CSS class that sets width.
data-height	      Explicit height of  BubbleText        200px, 30vh, auto	                Overrides any CSS class that sets height.
data-maxwidth	    Maximum width of BubbleText           400px, 80vw                       Restricts width when content would exceed it. 
                    	                                                                      Works alongside data-width.
data-maxheight	  Maximum height of BubbleText          300px, 50vh	                      Restricts height; if content overflows, 
                                                                                             scrollbars appear.
_Supports_ pixels: 300px, Percentages: 50% (relative to the containing block), Viewport units: 50vw, 30vh, Other CSS units: 20em,
    10rem, auto, etc. Important: _Do not use a bare number_ without a unit (e.g., "300"), as that would be invalid CSS
___________________________________________________________________________________________________________________________________________ 
Important notes:

-   center-height – The BubbleText is vertically centered within the page content area (or viewport if no .page is found). Any data-top value is ignored.
-   center-width – The BubbleText is horizontally centered within the page content area (or viewport). Any data-left value is ignored.
-   center-both – Both vertical and horizontal centering are applied; data-top and data-left are ignored.
-   The "@" value for edges only works when the BubbleText’s data-position is not one of the special modes (center-*, bottom-page). In those 
    modes, "@" is ignored for that axis because the mode overrides it.
-   The bottom-page mode uses data-bottom-gap to separate the BubbleText from the bottom of the page. The gap value can be in vh or px.
-   The centering modes (center-*) first try to place the BubbleText at the viewport center, then clamp it to keep it inside the page 
    (with a 10 px margin). This ensures the BubbleText never goes off‑screen.
-   The center-* modes can be combined with data-top/data-left/data-bottom/data-right to provide fallback vertical/horizontal positions 
    if clamping moves the BubbleText. For example, center-width uses the given top value (or bottom) for vertical placement, while the 
    horizontal position is centered.

_Standard BubbleText Inventory_________________________________________________________________________________________________________________
<span class="BubbleText-trigger" 
  data-top="5.5vh"   data-left="6.5vw"    data-height="20vh"   data-width="60vw"  data-animation="ZOOM"   
  data-tiptext="📌 BubbleText placed at Top and Bottom with Heightand Width, fading in "
  data-position="fixed">A Clickable word
</span>


Triming logic
--------------------------------------------------------------------------------------------------
  1. Get the page’s bounding rectangle relative to the viewport (pageRect).

  2. Define an inner padding (innerPadding = 10px) to keep the BubbleText away from the page edges.

  3. Convert the final top, left, height, width strings to pixel numbers (using toPixels).
        - If a value cannot be converted (e.g., calc()), that axis is skipped.

  4. Compute total dimensions including the BubbleText’s fixed padding/border (extra = 22px = 10px top/bottom padding + 1px top/bottom border × 2).
        - totalWidth = widthPx + extra (if widthPx is valid)
        - totalHeight = heightPx + extra (if heightPx is valid)

  5. Clamp top and left so the BubbleText’s outer box stays inside the page:
        - minTop = pageRect.top + innerPadding
        - maxTop = pageRect.bottom - totalHeight - innerPadding
        - If newTop < minTop, set to minTop; if newTop > maxTop, set to maxTop.
        (Similarly for left with minLeft / maxLeft.)

  6.fter repositioning, trim width/height if still overflowing:
        - Right edge overflow: availableWidth = pageRect.right - leftPx - innerPadding. If totalWidth > availableWidth, reduce content width:
          newContentWidth = max(0, availableWidth - extra) → update width (as a pixel string).
        - Bottom edge overflow: availableHeight = pageRect.bottom - topPx - innerPadding. If totalHeight > availableHeight, reduce content height similarly.
          Updated top, left, height, width strings (with px units) are then passed to toggleBubbleText.

Summary:
      ✅  data-top="@" data-left="@"  → Below clickable word, perfectly centered and Boundary Safe
          left, right and bottom
      ✅  data-top="center" data-left="center"  → Screen center
      ✅  Fixed positioning ( "30", "30%", "30px" ,  "10vh" , "calc(mixed_arithmentic)" )
      ✅  All animations (fade, bounce, slide, zoom) - DOn ont use....
      ✅  Text alignment ( data-textalign="center|right|left" )
      ✅  Responsive sizing (mobile/tablet/desktop)

 --------------------------------------------------------------------------------------------------




_END_______________________________________________________________________________________________________________________________________