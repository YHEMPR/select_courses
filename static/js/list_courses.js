$(document).ready(function() {
            fetchCourses(); // 载入课程数据

            $('.nav-link').click(function(event) {
                event.preventDefault(); // 阻止链接默认动作
                $('.nav-link').removeClass('active'); // 移除所有active类
                $(this).addClass('active'); // 为当前点击的链接添加active类
                $('.content-section').hide(); // 隐藏所有内容区域
                $($(this).data('target')).show(); // 显示目标内容区域

                if ($(this).data('target') === '#selected-courses') {
                    fetchSelectedCourses(); // 当需要时载入已选课程数据
                }
                 if ($(this).data('target') === '#transcript') {
                    fetchTranscript(); // 调用上面定义的函数加载并显示成绩单
                }
                if ($(this).data('target') === '#completed-courses') {
                    console.log("Fetching completed courses...");
                    fetchCompletedCourses(); // 当需要时载入已修课程数据
                }
            });

            $('#searchForm').submit(function(event) {
                event.preventDefault();
                fetchCourses($('#searchInput').val());
            });

            // 事件委托处理动态添加的选课和退课按钮
            $('#course-table-body').on('click', '.enroll-btn', function() {
                var courseId = $(this).data('course-id');
                enrollCourse(courseId);
            });

            $('#selected-course-table-body').on('click', '.drop-btn', function() {
                var courseId = $(this).data('course-id');
                dropCourse(courseId);
            });
        });

        function fetchCourses(query='') {
            $.ajax({
                url: `/student/api/courses?semester={{ semester }}&query=${query}`,
                type: 'GET',
                success: function(data) {
                    console.log(data)
                    $('#course-table-body').empty();
                    data.forEach(function(course, index) {
                        $('#course-table-body').append(`
                            <tr>
                                <th scope="row">${index + 1}</th>
                                <td>${course.course_id}</td>
                                <td>${course.course_name}</td>
                                <td>${course.credit}</td>
                                <td>${course.dept_name}</td>
                                <td>${course.teacher_name}</td>
                                <td>
                                    <button class="btn btn-primary enroll-btn" data-course-id="${course.course_id}">选课</button>
                                </td>
                            </tr>
                        `);
                    });
                },
                error: function() {
                    $('#course-table-body').append('<tr><td colspan="7">无法加载课程信息</td></tr>');
                }
            });
        }

        function fetchSelectedCourses() {
            $.ajax({
                url: '/student/api/selected_courses?semester={{ semester }}',
                type: 'GET',
                success: function(data) {
                    console.log(data)
                    $('#selected-course-table-body').empty();
                    var totalCredits = 0;
                    data.forEach(function(course) {
                        $('#selected-course-table-body').append(`
                            <tr>
                                <td>${course.course_id}</td>
                                <td>${course.course_name}</td>
                                <td>${course.class_time}</td>
                                <td>${course.teacher_name}</td>
                                <td>${course.staff_id}</td>
                                <td>${course.credit}</td>
                                <td>
                                    <button class="btn btn-danger drop-btn" data-course-id="${course.course_id}">退课</button>
                                </td>
                            </tr>
                        `);
                        totalCredits += parseInt(course.credit);
                    });
                    $('#total-credits').text(totalCredits);
                },
                error: function() {
                    $('#selected-course-table-body').append('<tr><td colspan="7">加载已选课程信息失败</td></tr>');
                }
            });
        }
        function fetchCompletedCourses() {
    $.ajax({
        url: '/student/api/completed_courses',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            // 清空已修课程表格的当前内容
            $('#completed-course-table-body').empty();

            // 检查是否成功获取到课程数据
            if (response.success) {
                var courses = response.courses;

                // 遍历返回的课程数组，为每个课程创建表格行
                courses.forEach(function(course) {
                    var row = '<tr>' +
                        '<td>' + course.course_id + '</td>' +
                        '<td>' + course.course_name + '</td>' +
                        '<td>' + course.semester + '</td>' +
                        '<td>' + course.teacher_name + '</td>' +
                        '<td>' + course.credit + '</td>' +
                        '<td>' + course.score + '</td>' +
                        '</tr>';
                    $('#completed-course-table-body').append(row);
                });
            } else {
                console.error("Error fetching completed courses: " + response.message);
                alert("无法加载已修课程数据，请稍后再试。");
            }
        },
        error: function(xhr, status, error) {
            console.error("Error fetching completed courses: " + error);
            alert("无法加载已修课程数据，请稍后再试。");
        }
    });
}


        function enrollCourse(courseId) {
            $.ajax({
                url: '/student/enroll_course',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ course_id: courseId, semester: "{{ semester }}" }),
                success: function(response) {
                    if (response.success) {
                        alert('选课成功！');
                        fetchSelectedCourses(); // 重新载入已选课程数据
                    } else {
                        alert('选课失败: ' + response.message);
                    }
                },
                error: function(xhr) {
                    var errorMsg = '选课请求失败。';
                    if(xhr.responseJSON && xhr.responseJSON.message) {
                        errorMsg += ' 错误信息: ' + xhr.responseJSON.message;
                    }
                    alert(errorMsg);
                }
            });
        }

        function dropCourse(courseId) {
            $.ajax({
                url: '/student/drop_course',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ course_id: courseId, semester: "{{ semester }}" }),
                success: function(response) {
                    if (response.success) {
                        alert('退课成功！');
                        fetchSelectedCourses(); // 重新载入已选课程数据
                    } else {
                        alert('退课失败: ' + response.message);
                    }
                },
                error: function() {
                    alert('退课请求失败。');
                }
            });
        }
       function fetchTranscript() {
            let semester = prompt("请输入您要查询的学期（例如：202401）:");
    if (!semester) {
        alert('您没有输入学期。');
        return;  // 如果没有输入，就不执行任何操作
    }
    $.ajax({
        url: '/student/api/transcript',  // 确保后端 API 支持 POST
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            semester: semester
        }),
        success: function(data) {
            console.log(data);
            if (data.success) {
                let htmlRows = '';
                data.courses.forEach(function(course) {
                    htmlRows += `<tr>
                                    <td>${course.course_id}</td>
                                    <td>${course.course_name}</td>
                                    <td>${course.staff_id}</td>
                                    <td>${course.credit}</td>
                                    <td>${course.score}</td>
                                    <td>${course.grade_point}</td>
                                 </tr>`;
                });
                $('#transcript tbody').html(htmlRows);
                $('#transcript').append(`<div class="average-grade-point"><p>平均绩点: ${data.average_grade_point.toFixed(2)}</p>`);
            } else {
                alert('无法加载成绩单，请稍后再试。');
            }
        },
        error: function(xhr, status, error) {
            console.error("Error fetching transcript: " + error);
            alert('无法加载成绩单，请稍后再试。');
        }
    });
}