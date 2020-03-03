//自定义弹框
function Toast(msg, duration) {
    duration = isNaN(duration) ? 3000 : duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText = "width: 60%;min-width: 150px;opacity: 0.7;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 5px;position: fixed;top: 40%;left: 20%;z-index: 999999;background: rgb(0, 0, 0);font-size: 13px;font-family: Arial, Helvetica, sans-serif;";
    document.body.appendChild(m);
    setTimeout(function () {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(m)
        }, d * 1000);
    }, duration);
}

var ROUTER = {
    'cheaters': {
        'total_status': 6
    }
}

Vue.component("listpage", {
    template: `
    <div id='main_block'>
        {{ dy_lines }}
		<div id='last_info'>
			全部数据量: {{ total }} </br>
			上次公布时间: {{ last_pub_time }} </br>
			上次公布标题: {{ last_pub_title }} 
		</div>
		<div id='search_box'>
			<input id='input_box' v-model="search_value">
        </div>
        
		<div id='cheaters_show'>
            <tr id="listpage_li" v-for="(line, index) in lines" >
                <td><span>{{ index+1 }}</span></td>
                <td><span>{{ line.b_name }}</span></td>
                <td><span>{{ line._pub_time }}</span></td>
            </tr>
		</div>
	</div>	
    `,
    data() {
        return {
            "total": "",
            "last_pub_time": "",
            "last_pub_title": "",
            "search_value": "",
            "lines": [],

        }
    },
    props: {
        api: String,
    },
    mounted() {
        //     this.updateView()
        console.log(this.api);

        // 加载大概信息
        axios.get('api/total_status').then(response => (
            this.total = response.data.data.total,
            this.last_pub_time = response.data.data.last_pub_time,
            this.last_pub_title = response.data.data.title
        )).catch(function (err) {
            console.log(err)
        })
    },
    methods: {
        getCheaters(key) {
            var res = '';
            axios.get('api/cheaters' + key.trim()).then(response => (
                console.log(response.data),
                // this.total = response.data.data.total,
                // this.last_pub_time = response.data.data.last_pub_time,
                // this.last_pub_title = response.data.data.title,
                res =  response.data.data
            )).catch(function (err) {
                console.log(err)
            });

            return  res

            if (key) {
                Toast('有key')
            } else {
                Toast('没有key');
            }
        }
    },
    // methods: {
    //     addRecv(to_add) {
    //         if (to_add) {
    //             var form = new FormData();
    //             form.append('account', to_add);
    //             axios.post(this.api_url, form).then(response => (
    //                 console.log(this.recvivers),
    //                 this.$set(this.recvivers, to_add, { "is_recv": 1 }),
    //                 Toast(response.data.msg)
    //             )).catch(function (err) {
    //                 console.log(err)
    //             })
    //         }
    //     },
    //     updateRecv(account, is_recv) {
    //         is_recv = is_recv ? 1 : 0;
    //         var form = new FormData();
    //         form.append('account', account);
    //         form.append('is_recv', is_recv);
    //         axios.put(this.api_url, form).then(response => (
    //             // console.log(this.mail_recvivers),
    //             Toast(this.response.data.msg)
    //         )).catch(function (err) {
    //             console.log(err)
    //         })
    //     },
    //     deleteRecv(account, index) {
    //         axios.delete(this.api_url + '?account=' + account).then(response => (
    //             Vue.delete(this.recvivers, account),
    //             Toast(this.response.data.msg)
    //         )).catch(function (err) {
    //             console.log(err)
    //         })
    //     },
    //     updateView() {
    //         // 加载收件人列表
    //         axios.get(this.api_url).then(response => (
    //             this.recvivers = response.data
    //         )).catch(function (err) {
    //             console.log(err)
    //         })
    //     },
    //     testSend() {
    //         // 加载收件人列表
    //         axios.get('/notice/test/' + this.api_url.split('/').pop()).then(response => (
    //             Toast(response.data.msg)
    //         )).catch(function (err) {
    //             console.log(err)
    //         })
    //     }
    // },
    computed: {
        // _updateView() {
        //     return this.updateView()
        // },
  
        dy_lines(){
            key = this.search_value.trim();
            console.log('key::::'+key);

            if (!this.search_value) {
                key = '*'
            };
            console.log('key::::'+key);

            axios.get('/api/cheaters/' + key).then(response => (
            // axios.get('/api/cheaters/' +'66').then(response => (
                console.log(response.data),
                // this.total = response.data.data.total,
                // this.last_pub_time = response.data.data.last_pub_time,
                // this.last_pub_title = response.data.data.title,
                this.lines=response.data.data,
                res =  response.data.data
                
            )).catch(function (err) {
                console.log(err)
            });
        }
    }
})


var main = new Vue({
    el: "#main",
    data: {

    },
    mounted() {
        // 邮箱配置
        // axios.get('/send/mail_backend').then(response => (
        //     this.send_mail_account = response.data.account,
        //     this.send_mail_password = response.data.password
        // )).catch(function (err) {
        //     console.log(err)
        // })

    },
    // methods: {
    //     updateSendMail() {
    //         var form = new FormData();
    //         form.append('account', this.send_mail_account);
    //         form.append('password', this.send_mail_password);
    //         axios.post('/send/mail_backend', form).then(response => (
    //             Toast(response.data.msg)
    //         )).catch(function (err) {
    //             console.log(err)
    //         })
    //     },
    //     clickTab(block_name) {
    //         // 点击tab，用于切换
    //         for (var key in this.is_show_map) {
    //             if (key === block_name) {
    //                 this.is_show_map[key] = !Boolean(this.is_show_map[key])
    //             } else {
    //                 this.is_show_map[key] = false
    //             }
    //         }
    //     },
    //     tabIsShow(block_name) {
    //         // 是否展示当前tab，用于切换
    //         return Boolean(this.is_show_map[block_name])
    //     }
    // },
    // computed: {
    //     b64encodeValue() {
    //         return window.btoa(this.b64raw)
    //     },

    // }
})