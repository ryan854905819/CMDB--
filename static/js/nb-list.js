/**
 * Created by Administrator on 2017/10/11.
 */

/*
自执行函数，只在前端有
(function (arg) {
    alert(arg)
})(666)

*/

(function (jq) {

    var requestUrl = "";
    var GLOBAL_CHOICES_DICT = {
        // 'status_choices': [[0,'xxx'],]
        // 'xxxx_choices': [[0,'xxx'],]
    };
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // 请求头中设置一次csrf-token
            if(!csrfSafeMethod(settings.type)){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });


    function getChoiceNameByid(choice_name,id) {
        var val;
        var status_choices_list = GLOBAL_CHOICES_DICT[choice_name];
        $.each(status_choices_list,function (kkkk,vvvv) {
            if(id == vvvv[0]){
                val = vvvv[1];
            }
        });
        return val;
    }

    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s,i) {
            return args[i];
        });
    };

    /*
    像后台获取数据
     */
    function init(pageNum) {
        $('#loading').removeClass('hide');
        var condition = getSearchCondition();
        console.log(condition);
        $.ajax({
            url:requestUrl,
            type: 'GET',
            data: {'pageNum':pageNum,'condition':JSON.stringify(condition)},
            dataType: 'JSON',
            success:function (response) {
                /* 处理choice */
                /*
                'global_choices_dict':{
            'status_choices':models.Server.server_status_choices
        }
                 */

                GLOBAL_CHOICES_DICT = response.global_choices_dict;

                 /* 处理搜索条件 */
                initSearchCondition(response.search_config);

                /* 处理表头 */
                initTableHead(response.table_config);
                /* 处理数据 */
                initTableBody(response.data_list,response.table_config);

                 /* 处理分页 */
                initPageHtml(response.page_html);

                $('#loading').addClass('hide');
            },
            error:function () {
                $('#loading').addClass('hide');
            }
        })


    }

     /*
    绑定搜索条件事件
     */
    function bindSearchConditionEvent(){

        /* 改变下拉框内容时*/
        $('#searchCondition').on('click','li',function () {
            // $(this) = li标签

            // 找到label文本修改
            $(this).parent().prev().prev().text($(this).text());

            // 找input标签，修改，重建
            $(this).parent().parent().next().remove();

            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if(type=='select'){
                var choice_name = $(this).find('a').attr('choice_name');

                // 生成下拉框，
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name',name);
                $.each(GLOBAL_CHOICES_DICT[choice_name],function(i,item){
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value',item[0]);
                    $(tag).append(op);
                })
            }else{
                // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">
                var tag = document.createElement('input');
                tag.setAttribute('type','text');
                // $(tag).addClass('form-control no-radius')
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder','请输入条件');
                tag.setAttribute('name',name);
            }

            $(this).parent().parent().after(tag);

        });
         /* 添加搜索条件 */
        $('#searchCondition .add-condition').click(function () {

            var $condition = $(this).parent().parent().clone();
            $condition.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('i').attr('class','fa fa-minus-square');

            // $(this).parent().parent().parent().append($condition);
            // $('#searchCondition').append($condition);
            $condition.appendTo($('#searchCondition'));
        });

        /* 删除搜索条件 */
        $('#searchCondition').on('click','.del-condition',function () {
            $(this).parent().parent().remove();
        });

         /* 点击搜索按钮 */
        $('#doSearch').click(function () {
            init(1);
        });

     }
     

    function initSearchCondition(searchConfig){
        //加上这个判断是为防止多次初始化，所以只要做一次初始化搜索条件后，页面切换条件不变
        if(!$('#searchCondition').attr('init')){
            var $ul = $('#searchCondition :first').find('ul');
            $ul.empty();

            //初始化默认搜索条件
            initDefaultSearchCondition(searchConfig[0]);
            $.each(searchConfig,function (i,item) {
                var li = document.createElement('li');
                var a =  document.createElement('a');
                a.innerHTML = item.title;
                a.setAttribute('name',item.name);
                a.setAttribute('type',item.type);
                if(item.type == 'select'){
                    a.setAttribute('choice_name',item.choice_name);
                }
                $(li).append(a);
                $ul.append(li);
            });

            $('#searchCondition').attr('init','true');
        }

    }

    //初始化搜索框
    function initDefaultSearchCondition(item) {
        // item={'name': 'hostname','title':'主机名','type':'input'},
        if(item.type == 'input'){
            var tag = document.createElement('input');
            tag.setAttribute('type','text');
            // $(tag).addClass('form-control no-radius')
            tag.className = "form-control no-radius";
            tag.setAttribute('placeholder','请输入条件');
            tag.setAttribute('name',item.name);

        }else{
            var tag = document.createElement('select');
            tag.className = "form-control no-radius";
            tag.setAttribute('name',item.name);
            $.each(GLOBAL_CHOICES_DICT[item.choice_name],function(i,row){
                var op = document.createElement('option');
                op.innerHTML = row[1];
                op.setAttribute('value',row[0]);
                $(tag).append(op);
            })
        }

        $('#searchCondition').find('.input-group').append(tag);
        $('#searchCondition').find('.input-group label').text(item.title);
    }

    function getSearchCondition() {
        // 找所有input,select
        // 作业：result数据格式为：
        /*
             {
                server_status_id: [1,2],
                hostname: ['c1.com','c2.com']
            }
         */
        var result = {};
        $('#searchCondition').find('input[type="text"],select').each(function(){
            var name = $(this).attr('name');
            var val = $(this).val();
            if(result[name]){
                result[name].push(val);
            }else{
                result[name] = [val ];
            }
        });
        return result;
    }

    function initPageHtml(page_html) {

        $('#pagination').empty().append(page_html);
    }

    function initTableHead(table_config) {
        /*
         table_config = [
                {
                    'q': 'hostname',
                    'title': '主机名',
                },
                {
                    'q': 'sn',
                    'title': '序列号',
                },
                {
                    'q': 'os_platform',
                    'title': '系统',
                },
            ]
         */
        //清除表格行，不然页面没有从新加载，在请求一次字段重复出现

        /*
        //conf 等于下面一个字典，k是列表的一个索引
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
         */


        $('#tHead tr').empty();
            $.each(table_config,function (k,conf) {
                if(conf.display) {
                    var th = document.createElement('th');
                    th.innerHTML = conf.title;
                    $('#tHead tr').append(th);
                }
            });
    }

    function initTableBody(data_list,table_config) {
        /*
        //data_list  下面数据
        [
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        ]

        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>

         */

        //不清空，每执行一次init()就会数据增加，因为是ajax请求，所以每次请求init前要把里面内容清空
        $('#tBody').empty();

        $.each(data_list,function (k,row_dict) {
            // {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},   //row_dict取到data_list里面每个字典，k是一个索引
            // {'hostname':'xx1', 'sn':'xx2', 'os_platform':'xxx2'},

            var tr = document.createElement('tr');
            /*

            //vv就是下面这个字典,kk是索引
            table_config
            {
            'q': None,
            'title': '选择',
             'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
            'attr':{'k':'v','edit':'true','od':'@id'},
        },
            */

            $.each(table_config,function (kk,vv) {

                if (vv.display) {
                        var td = document.createElement('td');
                        // td.innerHTML = row_dict[vv.q];   //vv.q // None,hostname,sn,os_platform
                        var format_dict = {};  //用来存放格式化好的数据
                        //vv.text.kwargs    就是这种字典{'nid': '@id'} ，kkk那的字典key，vvv拿字典的值

                    /* 处理Td内容 */
                    $.each(vv.text.kwargs, function (kkk, vvv) {
                            if(vvv.substring(0,2) == "@@"){
                                var name = vvv.substring(2,vvv.length); // status_choices
                                var val = getChoiceNameByid(name,row_dict[vv.q]);
                                format_dict[kkk] = val
                            }
                            else if (vvv[0] == "@") {
                                var name = vvv.substring(1, vvv.length);

                                //{'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},   //row_dict取到data_list里面每个字典，k是一个索引
                                //把{xxx}里面内容替换完成后加format_dict到字典里面去，row_dict[name]拿到是数据库取到的值
                                format_dict[kkk] = row_dict[name];
                            } else {
                                format_dict[kkk] = vvv;
                            }

                        });

                    //字符串进行格式化，把里面{xxx}占位符全部替换成出来，并且赋值给td标签
                        td.innerHTML = vv.text.tpl.format(format_dict);

                    /* 处理Td属性 */
                    /*
                     'attr':{'class': 'c1','k':'v','edit':'true','od':'@id'},
                     */
                    $.each(vv.attr,function (attrName,attrVal) {
                        if(attrVal[0] == '@'){
                            attrVal = row_dict[attrVal.substring(1,attrVal.length)];
                        }
                        td.setAttribute(attrName,attrVal);
                    });
                        $(tr).append(td);
                }
            });

            $('#tBody').append(tr);

        });

    }


    /* 进入编辑模式 */
    function trIntoEdit($tr){
        $tr.addClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this),需要进入编辑模式的td标签

            if($(this).attr('edit-type') == 'select' ){
                // select
                var choiceKey = $(this).attr('choice-key');
                var origin = $(this).attr('origin');
                // GLOBAL_CHOICES_DICT[choiceKey]
                /*
                [
                    [1,'xxx'],
                    [2,'xxx'],
                    [3,'xxx'],
                ]
                 */
                var tag = document.createElement('select');
                //添加一个样式
                tag.className = "form-control";
                $.each(GLOBAL_CHOICES_DICT[choiceKey],function (k,value) {
                    var op = document.createElement('option');
                    op.innerHTML = value[1];
                    op.value = value[0];
                    //取到默认值
                    if(value[0] == origin){
                        //把默认值设置为选中状态
                        op.setAttribute('selected','selected');
                    }
                    tag.appendChild(op);
                    // $(tag).append(op);
                });

            }else {
                // input
                var text = $(this).text();
                var tag = document.createElement('input');
                tag.setAttribute('type','text');
                tag.className = "form-control";
                tag.value = text;

            }
            $(this).html(tag);
        })



    }

    /* 退出编辑模式 */
    function trOutEdit($tr){
        $tr.removeClass('success');
        $tr.find('td[edit="true"]').each(function () {
            // $(this) 每一个td
            var origin = $(this).attr('origin');
            if($(this).attr('edit-type') == 'select'){

                var val = $(this).find('select').val();
                // var text = $(this).find('select')[0].selectedOptions[0].innerText;
                var text = $(this).find('select option[value="'+ val +'"]').text();
                $(this).attr('new-value',val);
                $(this).html(text);
            }else {
                var val = $(this).find('input').val();
                $(this).html(val);
            }
            //判断值是否改动
            if(origin != val){
                 $tr.attr('edit-status','true');
        }




        });
    }

    /*
    按钮组绑定事件
     */
    function bindBtnGroupEvent(){
        // 进入和退出编辑模式
        $('#editModeStatus').click(function () {
            if($(this).hasClass('btn-warning')){
                // 要退出编辑模式
                $(this).removeClass('btn-warning');
                $(this).text('进入编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEdit($tr);
                });

            }else {
                // 要进入编辑模式
                $(this).addClass('btn-warning');
                $(this).text('退出编辑模式');
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trIntoEdit($tr);
                });

            }
        });

        // 全选
        $('#checkAll').click(function () {
            // $('#tBody :checked')
            $('#tBody :checkbox').each(function () {
                if(!$(this).prop('checked')) {
                    // 选中值不能再操作，不然在选中状态下在点全选，就会有BUG
                    $(this).prop('checked', 'true');
                    // 进入编辑模式
                    if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trIntoEdit($tr);
                    }
                }
            });

        });

        //取消
        $('#checkCancel').click(function () {
            $('#tBody :checked').each(function () {
                // $(this),已经选中checkbox
                $(this).prop('checked',false);
                if($('#editModeStatus').hasClass('btn-warning')){
                    var $tr = $(this).parent().parent();
                    trOutEdit($tr);
                }
            })
        });

        //反选
        $('#checkReverse').click(function () {
            $('#tBody :checkbox').each(function () {
                 if($(this).prop('checked')){
                        //选中
                     $(this).prop('checked',false);
                     // 退出编辑模式
                     if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trOutEdit($tr);
                }
                 }else {
                     $(this).prop('checked',true);
                     if($('#editModeStatus').hasClass('btn-warning')){
                        var $tr = $(this).parent().parent();
                        trIntoEdit($tr);
                    }

                 }
            })
        });

        //删除
        $('#delMulti').click(function () {
            // 显示模态对话框
            // 给确定按钮绑定事件
            var ids =[];
            $('#tBody :checked').each(function () {
                ids.push($(this).val());
            });
             $.ajax({
                url: requestUrl,
                type: 'delete',
                data: JSON.stringify(ids),
                traditional:true,
                dataType: 'JSON',
                success:function (arg) {
                    if(arg.status){
                        // 显示正确信息
                        $('#handleStatus').text('执行成功');
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000);
                    }else{
                        // 显示错误信息
                        $('#handleStatus').text(arg.msg);

                    }
                }
            })

        });

        // 保存
        $('#saveMulti').click(function () {
            if($('#editModeStatus').hasClass('btn-warning')){
                $('#tBody :checked').each(function () {
                    var $tr = $(this).parent().parent();
                    trOutEdit($tr);
                    $('#editModeStatus').removeClass('btn-warning');
                    $('#editModeStatus').text('进入编辑模式');
                });

            }

            var update_dict = [
                // {'nid':1, 'hostname': 'c1.com'},
                // {'nid':2, 'hostname': 'c1.com'},
                // {'nid':3, 'hostname': 'c1.com'},
                // {'nid':4, 'hostname': 'c1.com'},
            ];
            $('#tBody tr[edit-status="true"]').each(function () {
                // $(this) 是每一个tr标签
                var tmp = {};
                tmp['nid'] = $(this).children().first().attr('nid');
                $(this).children('[edit="true"]').each(function () {
                    // $(this),是td
                    var origin = $(this).attr('origin');
                    var name =  $(this).attr('name');
                    if($(this).attr('edit-type') == 'select'){
                        var newVal = $(this).attr('new-value');
                    }else {
                        var newVal = $(this).text();
                    }
                    if(origin != newVal){
                        tmp[name] = newVal;
                    }
                });
                 update_dict.push(tmp);
            });
            // console.log(update_dict);
             // 通过Ajax提交后台
            $.ajax({
                url:requestUrl,
                type:'PUT',
                data:JSON.stringify(update_dict),
                dataType: 'JSON',
                success:function (arg) {
                    console.log(arg);
                     if(arg.status){
                        // 显示正确信息
                        $('#handleStatus').text('保存成功');
                        setTimeout(function () {
                            $('#handleStatus').empty();
                        },5000);
                    }else{
                        // 显示错误信息
                        $('#handleStatus').text(arg.msg);

                    }

                }
            });

        });


    }


    /*
    单独checkbox编辑模式绑定事件
     */
    function bindEditModeEvent() {
         /* checkbox 绑定事件*/
        $('#tBody').on('click',':checkbox',function () {
            // $(this) // checkbox标签
            // 1. 检测是否已经被选中
            if($('#editModeStatus').hasClass('btn-warning')){
                var $tr = $(this).parent().parent();
                if($(this).prop('checked')){
                    // 进入编辑模式
                    trIntoEdit($tr);
                }else{
                    // 退出编辑模式
                    trOutEdit($tr);
                }
            }

        });
    }

    ctrStatus = false;
    window.onkeydown = function (event) {
        if(event && event.keyCode == 17){
            ctrStatus = true;
        }
    };
    window.onkeyup = function (event) {
        if(event && event.keyCode ==17){
            ctrStatus = false;
        }
    };

    /* 给表格中的下拉框绑定chang事件 */
    function bindSelectChangeEvent(){
        $('#tBody').on('change','select',function () {
            if(ctrStatus){
                var v = $(this).val();
                var $tr = $(this).parent().parent();
                var index = $(this).parent().index();
                $tr.nextAll().each(function () {
                    if($(this).find(':checkbox').prop('checked')){
                        $(this).children().eq(index).children().val(v);
                    }
                })
            }
        })
    }


    jq.extend({
        "nBList":function (url) {
            requestUrl = url;
            init(1);
            //一加载就绑定搜索条件事件
            bindSearchConditionEvent();
            bindEditModeEvent();
            bindBtnGroupEvent();
            bindSelectChangeEvent();

        },

        "changePage":function (pageNum) {
            init(pageNum);
        }
    });

})(jQuery);




