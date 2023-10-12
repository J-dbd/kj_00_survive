function is_checked(obj_id, state) {
  $.ajax({
    type: "POST",
    url: "api/check",
    data: {
      obj_id: obj_id,
      state: state,
    },
    success: function (response) {
      location.reload();
    },
  });
}

function add_new_target(member_id = "KYUMIN", target_date = "2023-10-10") {
  $.ajax({
    type: "POST",
    url: "api/add_new_target",
    data: {
      member_id: member_id,
      target_date: target_date,
      text: document.getElementById("created_text").value,
    },
    success: function (response) {
      location.reload();
    },
  });
}

function delete_item(obj_id) {
  $.ajax({
    type: "POST",
    url: "api/delete_target",
    data: {
      obj_id: obj_id,
    },
    success: function (response) {
      location.reload();
    },
  });
}

function getDate() {
  $.ajax({
    type: "GET",
    url: "api/getDate",
    data: {},
    success: function (response) {
      let received_target_team_data = response["target_team"];
      let start_date = received_target_team_data[0]["start_date"];
      let end_date = received_target_team_data[0]["end_date"];
      let team_goal = received_target_team_data[0]["text"];
      initProjectTerm(start_date, end_date);
      initTeamGoal(team_goal);
    },
  });
}

function getTarget(id) {
  $("#calendar_date").empty();
  $.ajax({
    type: "GET",
    url: "/api/getTarget",
    data: {},
    success: function (response) {
      let target_data = response["targets"];
      var member_id_set = new Set();
      var before_date = target_data[0]["target_date"];
      const date_string_arr = Array.from({ length: 30 }, (_, index) =>
        (index + 1).toString().padStart(2, "0")
      );

      for (let j = 0; j < date_string_arr.length; j++) {
        initDate(date_string_arr[j], id);
      }

      for (let i = 0; i < target_data.length; i++) {
        let target = target_data[i];
        let member_id = target["member_id"];
        let target_date = target["target_date"];
        if (target_date != before_date) {
          let date = before_date.substr(-2);
          initMember(date, member_id_set);
          member_id_set = new Set();
        }

        before_date = target_date;
        member_id_set.add(member_id);

        if (i == target_data.length - 1) {
          let date = before_date.substr(-2);
          initMember(date, member_id_set);
        }
      }
    },
  });
}

function initDate(date, id) {
  let temp_html = `<div class="relative flex flex-col bg-white group">
                                        <span class="mx-2 my-1 text-xs font-bold">${date}</span>
                                        <div class="flex flex-col px-4 py-6" onclick="window.location.href='../target_list?_id=${id}&date=${date}'">
                                            <button 
                                                class="flex items-center flex-shrink-0 h-5 px-1 py-6 text-xs hover:bg-gray-200">
                                                <div>
                                                    <ul id="calender-${date}" class="list-disc my-6 mx-6">
                                                    </ul>
                                                </div>
                                            </button>
                                        </div>
                                    </div>`;
  $("#calendar_date").append(temp_html);
}

function initTeamGoal(team_goal) {
  $(`#team_goal_board`).empty();
  team_goal.forEach(function (goal) {
    let temp_html = `<div class="relative flex items-center mb-4 z-0">
                                <input type="text" id="disabled_standard" class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " disabled />
                                <label for="disabled_standard" class="absolute text-sm text-black dark:text-gray-500 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">${goal}</label>
                                <input id="default-checkbox" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                        </div>`;
    $(`#team_goal_board`).append(temp_html);
  });
}

function initNewTeamGoal(new_team_goal) {
  let temp_html = `<div class="relative flex items-center mb-4 z-0">
                    <input type="text" id="disabled_standard" class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " disabled />
                    <label for="disabled_standard" class="absolute text-sm text-black dark:text-gray-500 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">${new_team_goal}</label>
                    <input id="default-checkbox" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                </div>`;
  $(`#team_goal_board`).append(temp_html);
}

function postNewTeamGoal(start_date, end_date, team_number, new_team_goal) {
  $.ajax({
    type: "POST",
    url: "api/postNewTeamGoal",
    data: {
      start_date: start_date,
      end_date: end_date,
      team_number: team_number,
      text: new_team_goal,
    },
    success: function (response) {
      location.reload();
    },
  });
}

function initMember(date, member_id_set) {
  $(`#${date}`).empty();
  const member_id_arr = [...member_id_set];
  for (let i = 0; i < member_id_arr.length; i++) {
    var temp_html;
    if (i % 2) {
      temp_html = `<li>${member_id_arr[i]}</li>`;
    } else {
      temp_html = `<li>${member_id_arr[i]}</li>`;
    }
    $(`#calender-${date}`).append(temp_html);
  }
}

function initProjectTerm(start_date, end_date) {
  $("#start_to_end_date").empty();
  var temp_html = `${start_date} ~ ${end_date}`;
  $("#start_to_end_date").append(temp_html);
}

function initGroup(week) {
  let tempHtml = `<select id="week${week}_team" onchange="location.href='team_page'" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-green-700 dark:border-green-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 my-6">
                        <option selected>정글 3기 ${week}주차</option>`;
  $("#group_by_week").append(tempHtml);
}

function initTeam(week, team_number_arr) {
  for (let i = 0; i < team_number_arr.length; i++) {
    let tempHtml = `<option value="${team_number_arr[i]}">${team_number_arr[i]}</option>`;
    $(`#week${week}_team`).append(tempHtml);
  }
}
