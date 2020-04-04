import {shallowMount} from "@vue/test-utils";
import Composite from "@/components/Composite";

describe('Composite.vue', () => {

    it('プロパティの内容が描画されるかテスト', () => {
        const data = {pk: 1, name: 'django', zip_depth: 1}
        const wrapper = shallowMount(Composite, {
            propsData: { data }
        })
        expect(wrapper.text()).toMatch('1 django')
    })

    it('コンポジット名クリック時のテスト', ()=> {
        const wrapper = shallowMount(Composite, {
            propsData: {
                data: {pk: 1, name: 'python', zip_depth: 1, is_dir: true}
            }
        })
        wrapper.find('.composite-link').trigger('click')
        const emit = wrapper.emitted()

        expect(emit.click).toBeTruthy()
        expect(emit.click[0][0].name).toBe('python')
    })


    it('編集ボタンのテスト', ()=> {
        const wrapper = shallowMount(Composite, {
            propsData: {
                data: {pk: 1, name: '更新になってるはず', zip_depth: 1, is_dir: true},
                editable: true
            }
        })
        wrapper.find('.update').trigger('click')
        const emit = wrapper.emitted()

        expect(emit.update).toBeTruthy()
        expect(emit.update[0][0].name).toBe('更新になってるはず')
    })

    it('削除ボタンのテスト', ()=> {
        const wrapper = shallowMount(Composite, {
            propsData: {
                data: {pk: 1, name: '削除になってるはず', zip_depth: 1, is_dir: true},
                editable: true
            }
        })
        wrapper.find('.delete').trigger('click')
        const emit = wrapper.emitted()

        expect(emit.remove).toBeTruthy()
        expect(emit.remove[0][0].name).toBe('削除になってるはず')
    })

    it('zipリンクのテスト', ()=> {
        const wrapper = shallowMount(Composite, {
            propsData: {
                data: {pk: 1, name: 'zipになってるはず', zip_depth: 1, is_dir: true},
                editable: true,
                zipUrl: 'dummy'
            }
        })
       expect(wrapper.find('a.zip').attributes('href')).toBe('dummy')

    })

    it('zipリンクのテスト(zipリンクがないケース)', ()=> {
        const wrapper = shallowMount(Composite, {
            propsData: {
                data: {pk: 1, name: 'なし', zip_depth: 1, is_dir: true},
                editable: false
            }
        })
        expect(wrapper.find('a.zip').exists()).toBe(false)

    })

})