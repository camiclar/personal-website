# AI Prompts and Reflection

## Prompts
### Refactoring from hand-coded CSS to Bootstrap
- My prompt: This is my portfolio website. All of the styling is hand-coded using custom CSS. I would like to refactor it so that it uses Bootstrap. So please go through and if there are any areas in the CSS that can be accomplished more simply using Bootstrap, please update so it uses Bootstrap. The final output should visually look exactly the same, just have it use Bootstrap.
- AI output: It refactored my code to replace hand-coded styles with Bootstrap ones. It also removed redundant code.
- Note: The refactoring was done mostly successfully, but there was a minor responsiveness issue that I asked it to correct.

### Fixing responsiveness issue
- My prompt: That was pretty good, but there is a small issue with the project previews. So originally there was a breakpoint at about 768px for the width. Below 768px, it was flex-flow: row wrap. Above 768px, it's flex-flow: row-reverse nowrap. That change to flex-flow: row-reverse nowrap is no longer working. Can you fix it?
- AI output: It restored the original media query and removed its previous Boostrap for this section.
- Note: I accepted the output.

### Redoing navigation
- Okay now I want to redo the navigation. Currently, there are two completely separate nav bars: one for widescreen and one for mobile. I want to make it so that there is just one responsive nav bar. Use Bootstrap for this, but make it so that the widescreen version looks visually similar to the current widescreen nav bar. It's okay if the mobile navigation looks different from the current mobile navigation.
- AI output: It replaced the separate widescreen and mobile navbars with one responsive Bootstrap navbar with some custom styling.
- Note: The new navbar has some visual issues I don't like. I'll keep the AI solution for now but want to go back and fix it later.

### Adding images
- My prompt: Currently, only the iu-mobile.html project page has images on the actual page. However, there are images for all of the projects in the images folder. Please add in the images to the relevant pages. So phase1-home and bam-preview should go on building-a-mind.html. old-resource-library-filters, old-resource-library, and resource-library-preview should go on resource-library.html
- AI output: It added a new section to the two project pages with the images, consistent styling, and relevant copy.
- Note: I'm not a huge fan of the layout it created. I will keep the styling on the images but modify the layout.

### Adding resume
- My prompt: Create a new page resume.html (and update the resume link in the nav bar to point to it). This new page should have the @Clark_Camilla_Resume.pdf file embedded.
- AI output: It successfully embedded the PDF and added a button to download it.
- Note: I'm keeping the new page and embedded PDF, but the styling needs some adjusting.

### Fixing resume styling
- My prompt: Okay that's a good start, but on the resume.html page, the area where you view the resume is too thin. It looks like it's only showing up as around 305 pixels wide rather than the max-width of 1000. Can you fix that? Also can you please use the same styling for the download button as on the project pages (like the "See the finished product" button on building-a-mind.html). Currently it looks like there's no padding on the download resume button, and I want the font color to be white
- AI output: It fixed the issues I described, making the resume width wider and fixing the button styling.
- Note: I'm accepting the changes.

### Contact page
- My prompt: Create a contact.html page (and add a link to it in the nav bar). It should include my email (camiclar@iu.edu) my LinkedIn (https://www.linkedin.com/in/camilla-clark/) and  my github (https://github.com/camiclar ). Leave space at the bottom of the page for a contact form which we'll add later.
- It added the contact page as requested, complete with icons and consistent styling.
- Note: I'm accepting these changes.

### Contact form
- My prompt: Okay now we'll work on the contact form. Add a form on the contact.html page. - Fields: - First Name (required) - Last Name (required) - Email Address (required, valid format) - Password (required, min 8 characters) - Confirm Password (required, must match Password) - Use attributes: required, type, pattern, minlength. - Show clear error messages (using HTML or minimal JavaScript). - Redirect to a Thank You page (thankyou.html) after submission. - Accessibility requirement: All inputs must have labels connected with for and id. Add alt text for any images.
- It created the contact form, complete with validation and a thank you page.
- Note: I'm accepting most of the changes but the button styling needs adjusting.

## Reflection
I've been doing web design since the beginning of my undergraduate degree, yet this is essentially my first time using AI to assist with coding for it. I found it extremely useful for rapidly putting pages together and tweaking things where I don't quite remember what the syntax is. I found that it was not particularly good at making things visually look good or keeping with the style I created manually. I had to repeatedly ask it to use the same styling for buttons, and the layouts it created were not as intuitive as I would personally design them. That said, it is an extremely powerful tool and I cannot see myself not using it going forward.