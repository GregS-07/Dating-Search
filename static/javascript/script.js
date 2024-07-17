$(document).ready(() => {

    $(".card").css("display", "none");
    $(".card").each(function(index) {
            
        $(this).delay(150 * index).fadeIn(500); 

        $(this).on("click", () => {
            const link = $(this).data("link");
            const url = `profile_${link}`;
            window.location.href = url;
        })
    });

    // Fade in one at a time 
    $(".card").css("display", "none");
    $(".card").each(function(index) {
        if(index >= 10){
            $(this).addClass("excess")
        }else{
            $(this).delay(150 * index).fadeIn(500);  
        }
               
    
        // On click, open results page 
        $(this).on("click", () => {
            const link = $(this).data("link");
            const url = `profile_${link}`;
            window.location.href = url;
        })
    });
    
    $(".show-more").on("click", () => {
        if($(".excess").css("display") == "none"){
            $(".excess").css("display", "block");
            $(".show-more").html("Show less")
        }else{
            $(".excess").css("display", "none");
            $(".show-more").html("Show more")
        }
    
            })
    
    // Entering hobby list 
    $(".add-hobby").on("click", () => {
        let interest = $(".hobby-select").val();
        if(interest){
            let currentHobbies = $("#hobby-list").val().trim();
            if(currentHobbies && !currentHobbies.includes(interest)){
                $("#hobby-list").val(currentHobbies + " " + interest);
            }else{
                $("#hobby-list").val(interest);
            }
        }
    })
    
    $(".remove-hobby").on("click", () => {
        let interest = $(".hobby-select").val();
        let currentHobbies = $("#hobby-list").val().trim();
        if(currentHobbies && currentHobbies.includes(interest)){
            $("#hobby-list").val(currentHobbies.replace(interest, ""));
        }
    })
})