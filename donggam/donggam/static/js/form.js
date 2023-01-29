// 성인여부
$(function () {
    // type 이 radio 이고 id adult 인 input 을 click 했을 경우
    $('input[type="radio"][id="adult"]').on("click", function () {
        console.log("zzz");
        // startSetting 에 checked된 radio button의 value 값을 넣는다.
        var startSetting = $('input[type=radio][id="adult"]:checked').val();
        // startSetting이 later인 경우 style display를 flex로 변경한다.
        // d이면 미성인
        if (startSetting == "d") {
            $("#adult_name").css("display", "flex");
            $("#adult_num").css("display", "flex");
            $("#adult_line").css("display", "flex");
            // required 추가
            $("[name=parent_name]").attr("required", true);
            $("[name=parent_phone]").attr("required", true);
            alert(
                "신청자가 14세 미만의 아동인 경우 법정대리인의 동의가 필수사항이므로 확인 절차를 거친 후 신청 승인됩니다.법정대리인의 성명과 연락처를 입력해 주세요."
            );

            // 그외의 경우 style display를 none 으로 변경한다.
        } else {
            $("#adult_name").css("display", "none");
            $("#adult_num").css("display", "none");
            $("#adult_line").css("display", "none");
            $("[name=parent_name]").attr("required", false);
            $("[name=parent_phone]").attr("required", false);
        }
    });
});

// 체크확인
function checkDone() {
    // 인원체크하기
    num = $("[name=headcount]").val();
    agree = $("#no_agree").is(":checked");
    console.log(agree);
    if (num < 10 || num > 100) {
        alert("견학인원은 10명 이상 100명 이하만 신청 가능합니다.");
        return false;
    }
    if (agree === true) {
        alert(
            "개인정보 수집 및 이용자 동의사항에 동의하셔야 신청이 가능합니다."
        );
        return false;
    }
}

// 삭제시 다시 묻기
function realDel() {
    return confirm("삭제하시겠습니까?");
}

function realConf() {
    return confirm("저장하시겠습니까?");
}
function realConf() {
    return confirm("수정하시겠습니까?");
}

// 정기 공지 수정 버튼 클릭시
$(function () {
    $('input[type="submit"][id="edit_notice"]').on("click", function () {
        var startSetting = $('input[type="submit"][id="edit_notice"]').val();
        if (startSetting == "수정") {
            $('input[type="submit"][id="edit_notice"]').attr(
                "value",
                "수정완료"
            );
            $("#add_notice").css("display", "none");
            $("#notice_done_edit").css("display", "none");
            $("#notice_yet_edit").css("display", "inline");
        } else {
            // 수정으로 글 변경
            $('input[type="submit"][id="edit_notice"]').attr("value", "수정");
            $("#add_notice").css("display", "inline");
            alert("수정 완료 됐습니다.");
        }
    });
});

// 정기 공지 추가하기 버튼 클릭시
$(function () {
    $('input[type="submit"][id="add_notice"]').on("click", function () {
        $("#add_notice").css("display", "none");
        $("#edit_notice").css("display", "none");
        $("#add_info").css("display", "block");
    });
});

$(function () {
    $('input[type="submit"][id="save_notice"]').on("click", function () {
        $("#add_notice").css("display", "inline");
        $("#edit_notice").css("display", "inline");
        $("#add_info").css("display", "none");
    });
});
