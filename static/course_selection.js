// $(document).ready(function() {
//     fetchCourses(); // 载入课程数据
//     fetchSelectedCourses(); // 载入已选课程数据
//
//     // 处理搜索表单提交
//     $('#searchForm').submit(function(event) {
//         event.preventDefault();
//         fetchCourses($('#searchInput').val());
//     });
// });
//
// function fetchCourses(query='') {
//     $.ajax({
//         url: `/api/courses?semester={{ semester }}&query=${query}`,
//         type: 'GET',
//         success: function(data) {
//             $('#course-table-body').empty();
//             if (data.length === 0) {
//                 $('#course-table-body').append('<tr><td colspan="7">没有找到课程</td></tr>');
//             } else {
//                 data.forEach(function(course, index) {
//                     $('#course-table-body').append(`
//                         <tr>
//                             <th scope="row">${index + 1}</th>
//                             <td>${course.course_id}</td>
//                             <td>${course.course_name}</td>
//                             <td>${course.credit}</td>
//                             <td>${course.dept_name}</td>
//                             <td>${course.teacher_name}</td>
//                             <td>
//                                 <button class="btn btn-primary enroll-btn" data-course-id="${course.course_id}">选课</button>
//                             </td>
//                         </tr>
//                     `);
//                 });
//             }
//         },
//         error: function() {
//             $('#course-table-body').append('<tr><td colspan="7">加载课程数据失败</td></tr>');
//         }
//     });
// }
//
// function fetchSelectedCourses() {
//     $.ajax({
//         url: '/api/selected_courses?semester={{ semester }}',
//         type: 'GET',
//         success: function(data) {
//             $('#selected-course-table-body').empty();
//             var totalCredits = 0;
//             if (data.length === 0) {
//                 $('#selected-course-table-body').append('<tr><td colspan="7">没有已选课程</td></tr>');
//             } else {
//                 data.forEach(function(course) {
//                     $('#selected-course-table-body').append(`
//                         <tr>
//                             <td>${course.course_id}</td>
//                             <td>${course.course_name}</td>
//                             <td>${course.class_time}</td>
//                             <td>${course.teacher_name}</td>
//                             <td>${course.staff_id}</td>
//                             <td>${course.credit}</td>
//                             <td>
//                                 <button class="btn btn-danger drop-btn" data-course-id="${course.course_id}">退课</button>
//                             </td>
//                         </tr>
//                     `);
//                     totalCredits += parseInt(course.credit);
//                 });
//                 $('#total-credits').text(totalCredits);
//             }
//         },
//         error: function() {
//             $('#selected-course-table-body').append('<tr><td colspan="7">加载已选课程数据失败</td></tr>');
//         }
//     });
// }
